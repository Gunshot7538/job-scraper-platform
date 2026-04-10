import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_naukri_jobs(job_title, location, pages=3):

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

        # 🔍 SEARCH
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

        # 🔥 MULTI PAGE LOOP
        for page in range(pages):

            print(f"\n🚀 SCRAPING PAGE {page + 1}")

            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
            )

            # 🔥 SCROLL FULL PAGE (LAZY LOAD FIX)
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

            # 🔥 NEXT PAGE LOGIC (SCROLL + CLICK)
            if page < pages - 1:
                try:
                    print("➡️ MOVING TO NEXT PAGE...")

                    # scroll again before clicking next
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

                  # current URL save karo
                    old_url = driver.current_url

                    driver.execute_script("arguments[0].click();", next_btn)

                    print("✅ NEXT PAGE CLICKED")

                    # 🔥 wait until URL changes (IMPORTANT FIX)
                    wait.until(EC.url_changes(old_url))

                    # thoda extra safety wait
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

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time


# def scrape_naukri_jobs(job_title, location, pages=1):

#     options = uc.ChromeOptions()
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--start-maximized")

#     driver = uc.Chrome(options=options, version_main=146, use_subprocess=True)
#     wait = WebDriverWait(driver, 25)

#     all_jobs = []

#     try:
#         driver.get("https://www.naukri.com/")
#         time.sleep(5)

#         # 🔍 Search
#         search_job = wait.until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, "input[placeholder='Enter skills / designations / companies']")
#             )
#         )
#         search_job.clear()
#         search_job.send_keys(job_title)

#         search_loc = wait.until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, "input[placeholder='Enter location']")
#             )
#         )
#         search_loc.clear()
#         search_loc.send_keys(location)

#         search_btn = wait.until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "qsbSubmit"))
#         )
#         driver.execute_script("arguments[0].click();", search_btn)

#         time.sleep(6)

#         # 🔥 MULTI PAGE LOOP
#         for page in range(pages):

#             print(f"\n🚀 SCRAPING PAGE {page + 1}")

#             wait.until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
#             )

#             soup = BeautifulSoup(driver.page_source, "html.parser")
#             job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

#             print("JOBS FOUND:", len(job_cards))

#             for card in job_cards[:21]:
#                 try:
#                     title_tag = card.find("a", class_="title")
#                     company_tag = card.find("a", class_="comp-name")
#                     location_tag = card.find("span", class_="locWdth")
#                     experience_tag = card.find("span", class_="expwdth")
#                     posted_tag = card.find("span", class_="job-post-day")
#                     salary_tag = card.find("span", class_="sal-wrap")
#                     skills_tags = card.find_all("li", class_="tag-li")

#                     title = title_tag.get_text(strip=True) if title_tag else "Not Found"
#                     company = company_tag.get_text(strip=True) if company_tag else "Not Found"
#                     location_text = location_tag.get_text(strip=True) if location_tag else location
#                     experience = experience_tag.get_text(strip=True) if experience_tag else ""
#                     posted = posted_tag.get_text(strip=True) if posted_tag else ""
#                     salary = salary_tag.get_text(strip=True) if salary_tag else "Not Disclosed"

#                     skills = ", ".join(
#                         [s.get_text(strip=True) for s in skills_tags]
#                     ) if skills_tags else "Not Available"

#                     link = title_tag.get("href") if title_tag else ""

#                     # 🔥 detail page skip (stable scraping)
#                     job_type = "Not Available"
#                     requirements = "Not Available"
#                     description = "Not Available"

#                     all_jobs.append({
#                         "title": title,
#                         "company": company,
#                         "location": location_text,
#                         "salary": salary,
#                         "experience": experience,
#                         "skills": skills,
#                         "job_type": job_type,
#                         "posted_date": posted,
#                         "platform": "naukri",
#                         "requirements": requirements,
#                         "description": description,
#                         "apply_link": link,
#                     })

#                 except Exception as job_error:
#                     print("JOB ERROR:", job_error)

#             # 🔥 NEXT PAGE FIXED
#             if page < pages - 1:
#                 try:
#                     # scroll down (important)
#                     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                     time.sleep(2)

#                     # correct next button
#                     next_btn = wait.until(
#                         EC.element_to_be_clickable(
#                             (By.XPATH, "//a[@class='fright fs14 btn-secondary br2']")
#                         )
#                     )

#                     driver.execute_script("arguments[0].click();", next_btn)

#                     print("➡️ MOVED TO NEXT PAGE")

#                     time.sleep(6)

#                     # ensure next page loaded
#                     wait.until(
#                         EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
#                     )

#                 except Exception as e:
#                     print("❌ NEXT PAGE ERROR:", e)
#                     break

#     except Exception as e:
#         print("MAIN ERROR:", repr(e))

#     finally:
#         driver.quit()

#     return all_jobs

# # import undetected_chromedriver as uc
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from bs4 import BeautifulSoup
# # import time


# # def scrape_naukri_jobs(job_title, location, pages=1):
# #     options = uc.ChromeOptions()
# #     options.add_argument("--disable-blink-features=AutomationControlled")
# #     options.add_argument("--start-maximized")

# #     driver = uc.Chrome(options=options, version_main=146, use_subprocess=True)
# #     wait = WebDriverWait(driver, 25)
# #     all_jobs = []

# #     try:
# #         driver.get("https://www.naukri.com/")
# #         time.sleep(5)

# #         search_job = wait.until(
# #             EC.presence_of_element_located(
# #                 (By.CSS_SELECTOR, "input[placeholder='Enter skills / designations / companies']")
# #             )
# #         )
# #         search_job.clear()
# #         search_job.send_keys(job_title)
# #         time.sleep(2)

# #         search_loc = wait.until(
# #             EC.presence_of_element_located(
# #                 (By.CSS_SELECTOR, "input[placeholder='Enter location']")
# #             )
# #         )
# #         search_loc.clear()
# #         search_loc.send_keys(location)
# #         time.sleep(2)

# #         search_btn = wait.until(
# #             EC.element_to_be_clickable((By.CLASS_NAME, "qsbSubmit"))
# #         )
# #         driver.execute_script("arguments[0].click();", search_btn)
# #         time.sleep(6)

# #         wait.until(
# #             EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
# #         )

# #         # ✅ Pages loop — 1 page = 20 jobs
# #         for page_num in range(1, pages + 1):
# #             print(f"⏳ Scraping page {page_num} of {pages}...")

# #             soup = BeautifulSoup(driver.page_source, "html.parser")
# #             job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

# #             for card in job_cards:
# #                 try:
# #                     title_tag      = card.find("a", class_="title")
# #                     company_tag    = card.find("a", class_="comp-name")
# #                     location_tag   = card.find("span", class_="locWdth")
# #                     experience_tag = card.find("span", class_="expwdth")
# #                     posted_tag     = card.find("span", class_="job-post-day")
# #                     salary_tag     = card.find("span", class_="sal-wrap")
# #                     skills_tags    = card.find_all("li", class_="tag-li")

# #                     title         = title_tag.get_text(strip=True) if title_tag else "Not Found"
# #                     company       = company_tag.get_text(strip=True) if company_tag else "Not Found"
# #                     location_text = location_tag.get_text(strip=True) if location_tag else location
# #                     experience    = experience_tag.get_text(strip=True) if experience_tag else ""
# #                     posted        = posted_tag.get_text(strip=True) if posted_tag else ""
# #                     salary        = salary_tag.get_text(strip=True) if salary_tag else "Not Disclosed"
# #                     skills        = ", ".join([s.get_text(strip=True) for s in skills_tags]) if skills_tags else "Not Available"
# #                     link          = title_tag.get("href") if title_tag else ""

# #                     job_type     = "Not Available"
# #                     requirements = "Not Available"
# #                     description  = "Not Available"

# #                     if link:
# #                         try:
# #                             driver.execute_script("window.open(arguments[0]);", link)
# #                             driver.switch_to.window(driver.window_handles[-1])
# #                             time.sleep(3)

# #                             # ✅ Scroll karo taaki sab load ho
# #                             driver.execute_script("window.scrollTo(0, 500);")
# #                             time.sleep(1)
# #                             driver.execute_script("window.scrollTo(0, 1000);")
# #                             time.sleep(1)
# #                             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# #                             time.sleep(2)
# #                             driver.execute_script("window.scrollTo(0, 0);")
# #                             time.sleep(1)

# #                             detail_soup = BeautifulSoup(driver.page_source, "html.parser")

# #                             # ✅ Employment Type
# #                             details_divs = detail_soup.find_all(
# #                                 "div", class_=lambda c: c and "details" in c
# #                             )
# #                             for div in details_divs:
# #                                 label = div.find("label")
# #                                 if label and "Employment Type" in label.get_text():
# #                                     span = div.find("span")
# #                                     if span:
# #                                         job_type = span.get_text(strip=True)
# #                                     break

# #                             # ✅ Description + Requirements
# #                             desc_div = detail_soup.find(
# #                                 "div", class_=lambda c: c and "dang-inner-html" in c
# #                             )

# #                             if desc_div:
# #                                 full_text  = desc_div.get_text(" ", strip=True)
# #                                 lower_text = full_text.lower()

# #                                 req_keywords = [
# #                                     "requirements",
# #                                     "requirement",
# #                                     "what we're looking for",
# #                                     "qualifications"
# #                                 ]

# #                                 req_text  = "Not Available"
# #                                 desc_text = full_text

# #                                 for keyword in req_keywords:
# #                                     idx = lower_text.find(keyword)
# #                                     if idx != -1:
# #                                         desc_text = full_text[:idx].strip()
# #                                         req_text  = full_text[idx:].strip()
# #                                         break

# #                                 description  = desc_text[:500] if desc_text else full_text[:500]
# #                                 requirements = req_text[:600] if req_text != "Not Available" else "Not Available"

# #                             # ✅ Safe close
# #                             try:
# #                                 if len(driver.window_handles) > 1:
# #                                     driver.close()
# #                                     driver.switch_to.window(driver.window_handles[0])
# #                             except:
# #                                 pass
# #                             time.sleep(2)
# #                         except Exception as detail_error:
# #                             print("DETAIL ERROR:", detail_error)
# #                             try:
# #                                # Sabhi extra windows band karo
# #                                 while len(driver.window_handles) > 1:
# #                                     driver.switch_to.window(driver.window_handles[-1])
# #                                     driver.close()
# #                                 # Main window pe wapas jao
# #                                 driver.switch_to.window(driver.window_handles[0])
# #                             except Exception as recovery_error:
# #                                 print("RECOVERY ERROR:", recovery_error)
# #                                 # Session completely dead — loop tod do
# #                                 break

# #                     all_jobs.append({
# #                         "title":        title,
# #                         "company":      company,
# #                         "location":     location_text,
# #                         "salary":       salary,
# #                         "experience":   experience,
# #                         "skills":       skills,
# #                         "job_type":     job_type,
# #                         "posted_date":  posted,
# #                         "platform":     "naukri",
# #                         "requirements": requirements,
# #                         "description":  description,
# #                         "apply_link":   link,
# #                     })

# #                 except Exception as job_error:
# #                     print("JOB ERROR:", job_error)

# #             # ✅ Next page pe jao
# #             if page_num < pages:
# #                 try:
# #                     print(f"➡️ Next page pe ja raha hun...")
# #                     next_btn = driver.find_element(
# #                         By.CSS_SELECTOR, "a[class*='styles_next']"
# #                     )
# #                     driver.execute_script("arguments[0].click();", next_btn)
# #                     time.sleep(6)
# #                     wait.until(
# #                         EC.presence_of_element_located(
# #                             (By.CLASS_NAME, "srp-jobtuple-wrapper")
# #                         )
# #                     )
# #                 except Exception as next_err:
# #                     print(f"⚠️ Next page error: {next_err}")
# #                     break

# #     except Exception as e:
# #         print("MAIN ERROR:", repr(e))

# #     finally:
# #         driver.quit()

# #     print(f"✅ Total jobs scraped: {len(all_jobs)}")
# #     return all_jobs