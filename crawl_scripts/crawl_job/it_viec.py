from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def scrape_jobs_it_viec(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
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
            job_url = job.find('h3', class_='imt-3')['data-url']
            title = job.find('h3').text.strip()

            if any(keyword in title.lower() for keyword in ['senior', 'manager', 'leader', 'sr.', 'lead']):
                continue

            company = job.find(
                'div', class_='imy-3 d-flex align-items-center').span.text.strip()
            logo = job.find(
                'div', class_='imy-3 d-flex align-items-center').a.img['data-src']

            mode, location = [div.span.text.strip()
                            for div in job.find_all('div',
                                                    class_='d-flex align-items-center text-dark-grey imt-1')]

            tags = ' '.join([f'{a.text.strip()}' for a in job.find(
                'div', class_='imt-3 imb-2').find_all('a')])

            driver = webdriver.Chrome()
            driver.get(job_url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.close()

            try:
                job_description = soup.find_all('div', class_='imy-5 paragraph')[0]
                job_requirement = soup.find_all('div', class_='imy-5 paragraph')[1]
            except Exception:
                print(job_url)
                continue

            # Handle different types of list items (Some pages have ul and li, some pages have p)
            descriptions = [
                f"{li.get_text(strip=True)}"
                for ul in job_description.find_all("ul")
                for li in ul.find_all("li")
            ]
            descriptions += [
                f"{p.get_text(strip=True)}"
                for p in job_description.find_all("p")
            ]

            requirements = [
                f"{li.get_text(strip=True)}"
                for ul in job_requirement.find_all("ul")
                for li in ul.find_all("li")
            ]
            requirements += [
                f"{p.get_text(strip=True)}"
                for p in job_requirement.find_all("p")
            ]

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
            print("could not get job url")
            continue

    return job_data