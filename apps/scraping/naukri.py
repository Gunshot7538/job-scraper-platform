import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_naukri_jobs(job_title, location, pages=5):

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, version_main=146, use_subprocess=True)
    wait = WebDriverWait(driver, 25)

    all_jobs = []
    seen_links = set()

    try:
        driver.get("https://www.naukri.com/")
        time.sleep(5)

        # Search inputs
        search_job = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Enter skills / designations / companies']")
            )
        )
        search_job.clear()
        search_job.send_keys(job_title)

        search_loc = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Enter location']")
            )
        )
        search_loc.clear()
        search_loc.send_keys(location)

        search_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "qsbSubmit"))
        )
        driver.execute_script("arguments[0].click();", search_btn)

        time.sleep(6)

        # Handle pagination loop
        for page in range(pages):

            print(f"\n🚀 SCRAPING PAGE {page + 1}")

            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
            )

            # Scroll to trigger lazy loading
            last_height = driver.execute_script("return document.body.scrollHeight")

            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {last_height * (i+1)/5});")
                time.sleep(1.5)

            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

            print("JOBS FOUND:", len(job_cards))

            for card in job_cards[:25]:   # safe limit
                try:
                    title_tag = card.find("a", class_="title")
                    company_tag = card.find("a", class_="comp-name")
                    location_tag = card.find("span", class_="locWdth")
                    experience_tag = card.find("span", class_="expwdth")
                    posted_tag = card.find("span", class_="job-post-day")
                    salary_tag = card.find("span", class_="sal-wrap")
                    skills_tags = card.find_all("li", class_="tag-li")

                    title = title_tag.get_text(strip=True) if title_tag else "Not Found"
                    company = company_tag.get_text(strip=True) if company_tag else "Not Found"
                    location_text = location_tag.get_text(strip=True) if location_tag else location
                    experience = experience_tag.get_text(strip=True) if experience_tag else ""
                    posted = posted_tag.get_text(strip=True) if posted_tag else ""
                    salary = salary_tag.get_text(strip=True) if salary_tag else "Not Disclosed"

                    skills = ", ".join([s.get_text(strip=True) for s in skills_tags]) if skills_tags else "Not Available"
                    link = title_tag.get("href") if title_tag else ""

                    if link and link not in seen_links:
                        seen_links.add(link)

                        all_jobs.append({
                            "title": title,
                            "company": company,
                            "location": location_text,
                            "salary": salary,
                            "experience": experience,
                            "skills": skills,
                            "job_type": "Not Available",
                            "posted_date": posted,
                            "platform": "naukri",
                            "requirements": "Not Available",
                            "description": "Not Available",
                            "apply_link": link,
                        })

                except Exception as job_error:
                    print("JOB ERROR:", job_error)

            # Navigate to next page
            if page < pages - 1:
                try:
                    print("➡️ MOVING TO NEXT PAGE...")

                    # Scroll before clicking next
                    driver.execute_script("""
                    window.scrollTo({
                        top: document.body.scrollHeight - 300,
                        behavior: 'smooth'
                    });
                    """)
                    time.sleep(2)

                    next_btn = None

                    xpaths = [
                        "//a[span[text()='Next']]",
                        "//a[contains(text(),'Next')]",
                        "//a[@rel='next']"
                    ]

                    for xp in xpaths:
                        try:
                            next_btn = wait.until(
                                EC.element_to_be_clickable((By.XPATH, xp))
                            )
                            if next_btn:
                                break
                        except:
                            continue

                    if not next_btn:
                        print("❌ NEXT BUTTON NOT FOUND")
                        break

                    # Store current URL to track navigation
                    old_url = driver.current_url

                    driver.execute_script("arguments[0].click();", next_btn)

                    print("✅ NEXT PAGE CLICKED")

                    # Wait for navigation to complete
                    wait.until(EC.url_changes(old_url))

                    # Buffer for page load
                    time.sleep(3)

                except Exception as e:
                    print("❌ NEXT PAGE ERROR:", e)
                    break

    except Exception as e:
        print("MAIN ERROR:", repr(e))

    finally:
        driver.quit()

    print(f"\n✅ TOTAL JOBS SCRAPED: {len(all_jobs)}")

    return all_jobs

