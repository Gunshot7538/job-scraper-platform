import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import quote


def scrape_linkedin_jobs(job_title, location):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = None
    jobs = []

    try:
        print("Start Browsing here....")
        driver = uc.Chrome(options=options, use_subprocess=True, version_main = 146)
        wait = WebDriverWait(driver, 20)

        keywords = quote(job_title)
        loc = quote(location)

        url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={loc}&f_TPR=r604800"
        driver.get(url)
        time.sleep(random.uniform(4, 6))

        def close_popup():
            try:
                cross = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))
                )
                cross.click()
                time.sleep(1)
            except:
                pass

                    # 🔥 SCROLL TO LOAD MORE JOBS
            last_height = driver.execute_script("return document.body.scrollHeight")

            for i in range(5):   # 5 scroll = approx 40–60 jobs
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 3))

                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    print("No more new jobs loading")
                    break

                last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-search-card")

        print(f"Total jobs found: {len(job_cards)}")

        for card in job_cards:
            if len(jobs) >= 60:
                break
            try:
                title = ""
                company = ""
                location_text = ""
                posted_text = ""
                salary = ""
                experience = ""
                skills = ""
                job_type = ""
                requirements = ""
                description = ""

                title_tag = card.find("h3", class_="base-search-card__title")
                company_tag = card.find("h4", class_="base-search-card__subtitle")
                location_tag = card.find("span", class_="job-search-card__location")
                date_tag = card.find("time")

                title = title_tag.get_text(strip=True) if title_tag else "N/A"
                company = company_tag.get_text(strip=True) if company_tag else "N/A"
                location_text = location_tag.get_text(strip=True) if location_tag else "N/A"
                posted_text = date_tag.get_text(strip=True) if date_tag else ""

                link_tag = card.find("a", class_="base-card__full-link")
                if not link_tag or not link_tag.get("href"):
                    continue

                apply_link = link_tag.get("href")

                job_id = None
                match = re.search(r'/jobs/view/(\d+)', apply_link)
                if match:
                    job_id = match.group(1)

                # 🔥 clean valid URL
                if job_id:
                    apply_link = f"https://www.linkedin.com/jobs/view/{job_id}/"

                print("Title:", title)
                print("Company:", company)
                print("Location:", location_text)
                print("Posted:", posted_text)
                print("Link:", apply_link)

                driver.get(apply_link)
                time.sleep(random.uniform(3, 5))

                close_popup()
                close_popup()

                try:
                    show_btn = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Show more']"))
                    )
                    close_popup()
                    driver.execute_script("arguments[0].click();", show_btn)
                    time.sleep(2)
                except:
                    print("No show more button")

                close_popup()

                job_soup = BeautifulSoup(driver.page_source, "html.parser")
                page_text = job_soup.get_text(" ", strip=True)

                desc = job_soup.find("div", class_="show-more-less-html__markup")

                if desc:
                    description = desc.get_text(" ", strip=True)[:1500]
                else:
                    description = job_soup.get_text(" ", strip=True)[:1500]

                # CRITERIA
                criteria = job_soup.find_all("li", class_="description__job-criteria-item")

                seniority = ""
                employment = ""
                function = ""
                industry = ""

                for item in criteria:
                    label = item.find("h3")
                    value = item.find("span")

                    if label and value:
                        label_text = label.get_text(strip=True)
                        value_text = value.get_text(strip=True)

                        if "Seniority level" in label_text:
                            seniority = value_text
                        elif "Employment type" in label_text:
                            employment = value_text
                        elif "Job function" in label_text:
                            function = value_text
                        elif "Industries" in label_text:
                            industry = value_text

                # EXPERIENCE
                if seniority:
                    experience = seniority
                else:
                    exp_match = re.search(
                        r'(\d+\+?\s*(?:-|to)?\s*\d*\+?\s*years?)',
                        page_text,
                        re.IGNORECASE
                    )
                    if exp_match:
                        experience = exp_match.group(0)

                # JOB TYPE
                if employment:
                    emp_lower = employment.lower()
                    if "full" in emp_lower:
                        job_type = "full-time"
                    elif "part" in emp_lower:
                        job_type = "part-time"
                    elif "intern" in emp_lower:
                        job_type = "internship"
                    elif "contract" in emp_lower:
                        job_type = "contract"
                    else:
                        job_type = employment.lower()
                else:
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
                    elif "onsite" in lower_text or "on-site" in lower_text:
                        job_type = "onsite"

                
                skills_found = []

                skill_db = [
                    # Programming
                    "python","java","c++","c#",".net","golang","rust","php","ruby",

                    # Web
                    "html","css","javascript","react","angular","vue","next.js","node.js",

                    # Backend
                    "django","flask","spring boot","express","fastapi",

                    # Database
                    "sql","mysql","postgresql","mongodb","oracle",

                    # Cloud
                    "aws","azure","gcp","docker","kubernetes","terraform",

                    # Data
                    "pandas","numpy","machine learning","deep learning","tensorflow","pytorch",

                    # Tools
                    "git","github","jira","linux","bash",

                    # Non-tech
                    "sales","marketing","communication","leadership",
                    "excel","power bi","tableau","crm","accounting","finance",
                    "recruitment","hr","negotiation","customer service"
                ]

                if description:
                    desc_lower = description.lower()

                    # 🔥 match from DB
                    for skill in skill_db:
                        if skill in desc_lower:
                            skills_found.append(skill.upper())

                    # 🔥 extra patterns (API, services etc.)
                    extra_patterns = re.findall(r'\b[A-Za-z]{3,}\s?(?:API|apis|services|tools)\b', description)

                    for p in extra_patterns:
                        skills_found.append(p.strip())

                    # 🔥 clean result
                    skills_found = list(set(skills_found))[:10]

                    if skills_found:
                        skills = ", ".join(skills_found)
                    else:
                        skills = "Not Disclosed"
                else:
                    skills = "Not Disclosed"

                # SALARY
                salary_match = re.search(
                    r'(\$[\d,]+(?:\s*-\s*\$[\d,]+)?|\₹[\d,]+(?:\s*-\s*\₹[\d,]+)?|[\d,]+\s*(?:a year|a month|an hour))',
                    page_text,
                    re.IGNORECASE
                )
                if salary_match:
                    salary = salary_match.group(0)
                else:
                    salary = "Not Disclosed"

               

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "salary": salary,
                    "experience": experience,
                    "skills": skills,
                    "job_type": job_type,
                    "posted_date": posted_text,
                    "platform": "linkedin",
                    "description": description,
                    "apply_link": apply_link,
                }

                print("SCRAPED JOB:", job_data["title"])
                jobs.append(job_data)

            except Exception as e:
                print("Error while scraping LinkedIn job:", e)
                continue

        print("Total LinkedIn jobs scraped:", len(jobs))
        return jobs

    except Exception as e:
        print("Main LinkedIn error:", e)
        return []

    finally:
        if driver:
            driver.quit()
            print("Browser closed safely")