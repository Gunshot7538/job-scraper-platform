# 🚀 Smart Job Manager

<div align="center">
  <p>An intelligent, AI-powered platform designed to streamline the job search process by aggregating listings from top platforms and ranking them against your resume.</p>
</div>

---

## 📖 Overview

**Smart Job Manager** is a sophisticated Django-based web application that acts as your personal AI job search agent. Rather than manually scouring multiple job boards, this platform uses automated web scraping (Selenium) to fetch real-time listings from LinkedIn, Naukri, and Indeed. It then utilizes Natural Language Processing (NLP) to extract skills from your resume and assigns a **Smart Match Score** to every job, allowing you to focus on the roles you are most qualified for.

---

## ✨ Key Features

*   **🤖 AI-Powered Match Scoring**: Upload your resume, and the system automatically extracts your skills, experience, and location to rank incoming jobs based on relevance.
*   **🕷️ Multi-Platform Live Scraping**: Fetches up to 100+ fresh job listings per search directly from:
    *   LinkedIn
    *   Indeed
    *   Naukri
*   **📊 Executive Dashboard**: A clean, responsive, and glassmorphism-inspired UI to track scraped intelligence, average match scores, and application progress.
*   **🎨 Dynamic Theming System**: Built-in UI themes (Purple, Green, Gold, Light) with persistent user preferences.
*   **📄 Seamless Resume Parsing**: Intelligent keyword extraction system capable of reading `.pdf` and `.docx` files to build a comprehensive candidate profile.

---

## 🛠️ Technology Stack

*   **Backend Framework**: Python, Django 6.0
*   **Web Scraping & Automation**: Selenium WebDriver, BeautifulSoup
*   **Natural Language Processing**: spaCy (`en_core_web_sm`), Custom RegEx Extractors
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5 (for utility structure)
*   **Database**: SQLite (Development)

---

## 📸 Platform Interface

### 🏠 Homepage
A premium, SaaS-style landing page designed for conversion and clarity.
![Homepage](assets/home_page.PNG)

### 📊 Executive Dashboard
A centralized hub for initiating scrapes, managing resumes, and analyzing job matches.
![Dashboard](assets/dashboard_page.PNG)

### 📊 Platform Analytics
Detailed views of scraped job data with AI-generated relevance scores.
![Platform](assets/platform.PNG)

---

## 📁 System Architecture

```text
smart_job_manager/
├── apps/
│   ├── accounts/           # User authentication and session management
│   ├── dashboard/          # Core dashboard views and UI handlers
│   ├── jobs/               # Job models, logic, and database interactions
│   ├── resume_parser/      # PDF/Docx text extraction and NLP skill matching
│   └── scraping/           # Selenium bot scripts for LinkedIn, Indeed, Naukri
├── config/                 # Core Django project settings and routing
└── templates/              # Responsive HTML templates with dynamic styling
```

---

## ⚙️ Local Setup & Installation

Follow these steps to run the project locally on your machine.

**1. Clone the repository**
```bash
git clone https://github.com/your-username/job-scraper-platform.git
cd job-scraper-platform
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Install NLP Models**
```bash
python -m spacy download en_core_web_sm
```

**4. Run Migrations & Start Server**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
> The application will be accessible at `http://127.0.0.1:8000/`.

---

## ⚠️ Important Configuration Notes

*   **Selenium WebDriver**: Ensure you have [ChromeDriver](https://chromedriver.chromium.org/downloads) installed and added to your system's PATH. The version must match your installed Google Chrome browser.
*   **Environment Variables**: Create a `.env` file in the root directory to store sensitive configurations (e.g., SMTP email credentials for the export functionality).

---

## 🚀 Future Roadmap

*   **Advanced AI Analysis**: Integration with OpenAI/LLMs for deeper contextual resume-to-job matching.
*   **Automated Applications**: Scripts to automatically apply to jobs that score above a 90% match threshold.
*   **PostgreSQL Migration**: Upgrading the database for production-grade concurrency handling.

---

## 👨‍💻 Developed By

**Gautam Kumawat**  
Passionate software engineer focused on building intelligent, scalable web applications.

---

<div align="center">
  <i>If you found this project interesting or helpful, please consider giving it a ⭐ on GitHub!</i>
</div>
 