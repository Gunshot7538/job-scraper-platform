# Smart Job Manager

A Django-based web application that scrapes job listings from multiple platforms and displays them in a clean dashboard for easy access and tracking.

---

## Features

* Scrapes jobs from multiple platforms:

  * Indeed
  * LinkedIn
  * Naukri
* Stores job data in database
* Displays jobs in a structured dashboard
* Basic resume parsing (keyword-based)

---

## Tech Stack

* Python
* Django
* Selenium
* SQLite
* HTML, CSS, Bootstrap

---

## Project Structure

```
apps/
├── accounts        # Authentication (login/signup)
├── jobs            # Job data models & logic
├── dashboard       # Dashboard UI
├── scraping        # Scraping scripts
├── resume_parser   # Resume processing
```

---

## Screenshots

![Dashboard](assets/dashboard.png)

---

## Setup Instructions

```bash
git clone https://github.com/your-username/job-scraper-platform.git
cd job-scraper-platform
pip install -r requirements.txt
python manage.py runserver
```

---

## Important Notes

* Sensitive files like `.env`, database, and logs are excluded from the repository
* ChromeDriver is not included and should be set up locally

---

## Author

Gautam Kumawat
