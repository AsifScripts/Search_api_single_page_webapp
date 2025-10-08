# ------------------------
# FILE: core/views.py
# ------------------------
import csv
import io
import logging
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

VALUESERP_ENDPOINT = "https://api.valueserp.com/search"

def parse_valueserp_response(json_data):
    """
    Try to extract a list of results from ValueSERP-like responses.
    Return list of dicts: {title, link, snippet}
    This function is defensive: it checks multiple possible keys.
    """
    candidates = []
    # Common key names
    for key in ("organic_results", "organic", "results", "search_results", "items"):
        if isinstance(json_data, dict) and key in json_data:
            maybe = json_data.get(key) or []
            if isinstance(maybe, list):
                candidates = maybe
                break
    # Fallback: if the top-level 'result' looks like a list
    if not candidates and isinstance(json_data, list):
        candidates = json_data

    results = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        title = item.get('title') or item.get('name') or item.get('heading') or ''
        link = item.get('link') or item.get('url') or item.get('display_url') or ''
        snippet = item.get('snippet') or item.get('description') or item.get('snippet_text') or item.get('summary') or ''
        # sometimes ValueSERP contains nested 'snippet' as dict
        if isinstance(snippet, dict):
            snippet = snippet.get('text', '') or str(snippet)
        results.append({'title': title, 'link': link, 'snippet': snippet})
    return results

@require_http_methods(["GET", "POST"])
def index(request):
    """
    GET: show form
    POST: collect queries, call ValueSERP per query, display results
    """
    context = {'results_grouped': [], 'errors': [], 'queries_submitted': []}

    if request.method == 'POST':
        raw_queries = request.POST.getlist('query')
        # normalize: strip and keep non-empty
        queries = [q.strip() for q in raw_queries if q and q.strip()]
        context['queries_submitted'] = queries

        if not queries:
            context['errors'].append("Please enter at least one search keyword.")
            return render(request, 'core/index.html', context)

        api_key = settings.VALUESERP_API_KEY
        if not api_key:
            context['errors'].append("Server error: ValueSERP API key is not configured. Put VALUESERP_API_KEY in .env.")
            return render(request, 'core/index.html', context)

        all_results = []
        for q in queries:
            entry = {'query': q, 'results': [], 'error': None}
            try:
                params = {'api_key': api_key, 'q': q}
                resp = requests.get(VALUESERP_ENDPOINT, params=params, timeout=8)
                if resp.status_code != 200:
                    entry['error'] = f"API returned status {resp.status_code}"
                    logger.warning("ValueSERP non-200: %s %s", resp.status_code, resp.text)
                else:
                    data = resp.json()
                    parsed = parse_valueserp_response(data)
                    if not parsed:
                        entry['results'] = []
                    else:
                        # attach rank numbers
                        entry['results'] = [
                            {'rank': idx+1, 'title': r.get('title', ''), 'link': r.get('link', ''), 'snippet': r.get('snippet', '')}
                            for idx, r in enumerate(parsed)
                        ]
                # store for session CSV
            except requests.Timeout:
                entry['error'] = "API timeout"
            except requests.RequestException as e:
                entry['error'] = f"API error: {str(e)}"
            except ValueError:
                entry['error'] = "Invalid JSON from API"
            all_results.append(entry)

        # Save results in session for download
        request.session['last_search_results'] = all_results
        request.session.modified = True
        context['results_grouped'] = all_results

    return render(request, 'core/index.html', context)


def download_csv(request):
    """
    Read session['last_search_results'] and return CSV.
    """
    results = request.session.get('last_search_results')
    if not results:
        # redirect to home with simple message
        response = HttpResponse("No results to download. Do a search first.", content_type="text/plain")
        response.status_code = 400
        return response

    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)

    # header
    writer.writerow(['query', 'rank', 'title', 'link', 'snippet'])

    for group in results:
        q = group.get('query', '')
        if group.get('error'):
            writer.writerow([q, '', f"ERROR: {group['error']}", '', ''])
            continue
        rows = group.get('results') or []
        if not rows:
            writer.writerow([q, '', 'No results', '', ''])
            continue
        for r in rows:
            writer.writerow([q, r.get('rank', ''), r.get('title', ''), r.get('link', ''), r.get('snippet', '')])

    csv_bytes = buffer.getvalue().encode('utf-8')
    buffer.close()

    ts = timezone.now().strftime("%Y%m%d-%H%M%S")
    filename = f"search_results_{ts}.csv"
    res = HttpResponse(csv_bytes, content_type='text/csv; charset=utf-8')
    res['Content-Disposition'] = f'attachment; filename="{filename}"'
    return res
