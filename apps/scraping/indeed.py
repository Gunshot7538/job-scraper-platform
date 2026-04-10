import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random
import re


def scrape_indeed_jobs(job_title, location):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = None
    jobs = []

    try:
        print("Browser start here ....")
        driver = uc.Chrome(options=options , version_main = 146)

        url = "https://www.indeed.com/"
        driver.get(url)

        time.sleep(random.uniform(4, 6))

        print("Typing job title...")
        search_job = driver.find_element(By.NAME, "q")
        search_job.clear()
        search_job.send_keys(job_title)

        time.sleep(random.uniform(1, 2))

        print("Typing location...")
        search_loc = driver.find_element(By.NAME, "l")
        search_loc.send_keys(Keys.CONTROL + "a")
        search_loc.send_keys(Keys.DELETE)
        search_loc.send_keys(location)

        time.sleep(random.uniform(1, 2))
        search_loc.send_keys(Keys.ENTER)

        print("Searching...")

        wait_time = random.uniform(5, 10)
        print(f"Waiting for {wait_time:.2f} seconds...")
        time.sleep(wait_time)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(2, 4))

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")

        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards[:10]:
            try:
                title_tag = card.find("h2", class_="jobTitle")
                title = title_tag.get_text(strip=True) if title_tag else "Not Found"

                company_tag = card.find("span", {"data-testid": "company-name"})
                company = company_tag.get_text(strip=True) if company_tag else "Not Found"

                location_tag = card.find("div", {"data-testid": "text-location"})
                loc = location_tag.get_text(strip=True) if location_tag else "Not Found"

                link_tag = card.find("a", class_="jcs-JobTitle")
                if link_tag and link_tag.get("href"):
                    apply_link = "https://www.indeed.com" + link_tag.get("href")
                else:
                    apply_link = "https://www.indeed.com/"

                salary_tag = card.find(string=re.compile(r"\$|₹|a year|a month|an hour", re.I))
                salary = salary_tag.strip() if salary_tag else "Salary not mentioned"

                posted_date = ""
                posted_tag = card.find("span", {"data-testid": "myJobsStateDate"})
                if posted_tag:
                    posted_date = posted_tag.get_text(strip=True)
                else:
                    small_texts = card.find_all(["span", "div"])
                    for t in small_texts:
                        txt = t.get_text(" ", strip=True).lower()
                        if "today" in txt or "just posted" in txt or "days ago" in txt or "day ago" in txt or "hours ago" in txt:
                            posted_date = t.get_text(" ", strip=True)
                            break

                description = ""
                experience = ""
                skills = ""
                job_type = ""
                requirements = ""

                if apply_link != "https://www.indeed.com/":
                    driver.get(apply_link)
                    time.sleep(random.uniform(5, 7))

                    html = driver.page_source
                    soup2 = BeautifulSoup(html, "html.parser")
                    page_text = soup2.get_text(" ", strip=True)

                    # Description
                    desc = soup2.find("div", id="jobDescriptionText")
                    if not desc:
                        desc = soup2.find("div", {"class": "jobsearch-jobDescriptionText"})
                    if desc:
                        description = desc.get_text(separator=" ", strip=True)[:1500]

                    # Experience
                    exp_match = re.search(
                        r'(\d+\+?\s*(?:-|to)?\s*\d*\+?\s*years?)',
                        page_text,
                        re.IGNORECASE
                    )
                    if exp_match:
                        experience = exp_match.group(0)
                    else:
                        experience = "Not mentioned"

                    # Skills
                    skills_found = []
                    common_skills = [
                        "Python", "Java", "SQL", "Django", "Flask", "AWS", "Azure",
                        "JavaScript", "React", "HTML", "CSS", "Selenium", "Git",
                        "Pandas", "NumPy", "REST API", "Machine Learning", "Docker",
                        "Kubernetes", "Linux", "MySQL", "PostgreSQL"
                    ]

                    for skill in common_skills:
                        if re.search(rf"\b{re.escape(skill)}\b", page_text, re.IGNORECASE):
                            skills_found.append(skill)

                    if skills_found:
                        skills = ", ".join(skills_found)

                    # Job type
                    lower_text = page_text.lower()
                    if "full-time" in lower_text or "full time" in lower_text:
                        job_type = "full-time"
                    elif "part-time" in lower_text or "part time" in lower_text:
                        job_type = "part-time"
                    elif "internship" in lower_text:
                        job_type = "internship"
                    elif "contract" in lower_text:
                        job_type = "contract"
                    elif "remote" in lower_text:
                        job_type = "remote"
                    elif "hybrid" in lower_text:
                        job_type = "hybrid"
                    elif "on-site" in lower_text or "onsite" in lower_text:
                        job_type = "onsite"
                    else:
                        job_type = ""

                    # Requirements
                    if desc:
                        li_tags = desc.find_all("li")
                        req_list = []
                        for li in li_tags[:8]:
                            txt = li.get_text(" ", strip=True)
                            if txt:
                                req_list.append(txt)

                        if req_list:
                            requirements = " | ".join(req_list)

                    driver.back()
                    time.sleep(random.uniform(3, 5))

                job_data = {
                    "title": title,
                    "company": company,
                    "location": loc,
                    "salary": salary,
                    "experience": experience,
                    "skills": skills,
                    "job_type": job_type,
                    "posted_date": posted_date,
                    "platform": "indeed",
                    "requirements": requirements,
                    "description": description,
                    "apply_link": apply_link,
                }

                print("SCRAPED JOB:", job_data["title"])
                jobs.append(job_data)

            except Exception as e:
                print("Error while scraping job:", e)
                continue

        print("Total jobs scraped:", len(jobs))
        return jobs

    except Exception as e:
        print("Main program error:", e)
        return []

    finally:
        if driver:
            driver.quit()
            print("Browser closed safely")