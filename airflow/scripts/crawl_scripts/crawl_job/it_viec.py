import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_jobs_it_viec(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    # Automatically download and install ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)
    # filter_button = driver.find_element(By.XPATH,
    #                                     """/html/body/main/div[1]/div[2]/div[2]/div[3]/div/div[1]/div/div/button""")
    # filter_button.click()
    # time.sleep(1)
    # fresher_label = driver.find_element(By.XPATH,
    #                                     """//*[@id="filter_job"]/div/div/div[2]/form/section[1]/div/label[1]""")
    # fresher_label.click()
    # junior_label = driver.find_element(By.XPATH,
    #                                    """//*[@id="filter_job"]/div/div/div[2]/form/section[1]/div/label[2]""")
    # junior_label.click()
    # apply_button = driver.find_element(By.XPATH,
    #                                    """//*[@id="filter_job"]/div/div/div[3]/button""")
    # apply_button.click()
    # time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all('div', class_='ipy-2')
    driver.close()

    job_data = []

    for job in jobs:
        try:
            job_url = job.find('h3', class_='imt-3 text-break')['data-url']

            title = job.find('h3').text.strip()

            company = job.find(
                'div', class_='imy-3 d-flex align-items-center').span.text.strip()

            logo = job.find(
                'div', class_='imy-3 d-flex align-items-center').a.img['data-src']
            mode = job.find('div', class_='text-rich-grey flex-shrink-0').text.strip()
            
            location = job.find('div', class_='text-rich-grey text-truncate text-nowrap stretched-link position-relative')['title']
            
            tags = ', '.join([f'{a.text.strip()}' for a in job.find(
                'div', class_='imt-4 imb-3 d-flex igap-1').find_all('a')])

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(job_url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.close()

            try:
                job_description = soup.find_all('div', class_='imy-5 paragraph')[0]
                job_requirement = soup.find_all('div', class_='imy-5 paragraph')[1]
            except Exception:
                print(f"Could not get job description or requirement {job_url}")
                continue

            descriptions = ' '.join([
                f"{p.get_text(strip=True)}"
                for p in job_description.find_all("li")
            ]) or ' '.join([
                f"{p.get_text(strip=True)}"
                for p in job_description.find_all("p")
            ])

            requirements = ' '.join([
                f"{p.get_text(strip=True)}"
                for p in job_requirement.find_all("li")
            ]) or ' '.join([
                f"{p.get_text(strip=True)}"
                for p in job_requirement.find_all("p")
            ])

            job_data.append({
                'title': title,
                'company': company,
                'logo': logo,
                'url': job_url,
                'location': location,
                'mode': mode,
                'tags': tags,
                'descriptions': descriptions,
                'requirements': requirements
            })
        except Exception:
            print("Error processing job, skipping...")
            continue

    return job_data