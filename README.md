# Simple Django POC using ValueSERP

This web application is a simple proof-of-concept (POC) built using Python Django.
It allows users to enter one or more search keywords, then uses the ValueSERP API to fetch real-time Google search results for each keyword.

The app displays the results (title, link, and snippet) neatly in a table on the same page, and also provides an option to download the results as a CSV file.

#### It’s designed to demonstrate:

- API integration (ValueSERP → Django backend)

- Handling multiple user inputs dynamically

- Processing and displaying JSON API responses

- Exporting structured data as CSV


## Requirements 
https://drive.google.com/file/d/1PRShg6U0f9EuUX7wrKy7MLKpCFb5cXf8/view?usp=sharing

## Prerequisites

- Python 3.8 or higher
- Git (optional, if cloning from repository)

---

## Setup Instructions

### 1. Clone the Repository (if not already)

#### bash
- git clone https://github.com/AsifScripts/Search_api_single_page_webapp.git
- cd Search_api_single_page_webapp

### 2. Create a Virtual Environment

- It is recommended to use a virtual environment to manage dependencies.

#### Using venv
- python -m venv venv

#### Activate virtual environment
##### On Windows
- venv\Scripts\activate

##### On macOS/Linux
- source venv/bin/activate

### 3. Install Dependencies
- pip install -r requirements.txt

### 4. Configure Environment Variables

- Copy the example .env file and edit it with your credentials/configuration:
#### Bash
- cp .env.example .env

### 5. Apply Database Migrations

- python manage.py migrate

### 6. Run the Development Server
- python manage.py runserver

- Now your Django app should be running at http://127.0.0.1:8000

## Home page (Add multiple keyword, search, remove and downnload file as CSV)
<img width="1638" height="379" alt="image" src="https://github.com/user-attachments/assets/2ee00f82-acb2-41a8-a748-d0d3ddabf012" />

## single Keyword search (cat)
<img width="1716" height="909" alt="image" src="https://github.com/user-attachments/assets/3c23f681-3143-4326-b397-d6f0b7c81baf" />


## Multi value search
<img width="1675" height="864" alt="image" src="https://github.com/user-attachments/assets/db65d759-6d12-4b8c-9ac3-aab60ff75b6c" />
<img width="1642" height="836" alt="image" src="https://github.com/user-attachments/assets/91e99c33-8413-4bef-99bf-d761875ee12c" />

## Download csv file (session based)
<img width="1744" height="590" alt="image" src="https://github.com/user-attachments/assets/bdecb0f3-b22b-421b-92e0-44e322fa7673" />

## Handle cases
### Empty Keyword
<img width="1673" height="256" alt="image" src="https://github.com/user-attachments/assets/33f705c9-ec9a-4bda-be44-4fa11e088ef7" />

### Random query - No data return
<img width="1625" height="485" alt="image" src="https://github.com/user-attachments/assets/6c9ed335-9dc3-4ca1-8663-4ebe32f45836" />

### API error
<img width="1728" height="418" alt="Screenshot 2025-10-08 144414" src="https://github.com/user-attachments/assets/c8dbbb00-0693-477a-a58d-3e9559c7e72d" />




