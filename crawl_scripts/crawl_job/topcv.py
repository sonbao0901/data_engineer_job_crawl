from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def init_webdriver(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver

def scrape_jobs_topcv(url):
    driver = init_webdriver(url)
    time.sleep(3)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")
    jobs = soup.find_all('div', class_='job-item-search-result')
    driver.quit()

    job_data = []
    for job in jobs:
        title = job.find('h3').text.strip()
        company = job.find('a', class_='company').text.strip()
        try:
            logo = job.find('img')['src']
        except Exception:
            logo = job.find('img')['data-src']
        job_url = job.find('a')['href']
        location = job.find('label', class_='address').text.strip()
        salary = job.find('label', class_='title-salary').text.strip()
        
        # Initialize descriptions and requirements with default values
        descriptions = ''
        requirements = ''
        
        driver = init_webdriver(job_url)
        time.sleep(3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        divs = soup.find_all('div', class_='box-info')
        driver.quit()

        for div in divs:
            h2_tag = div.find('h2')     
            if h2_tag and "Mô tả công việc" in h2_tag.text.strip():
                li_content = [li.text.strip() for li in div.find_all('li')]
                descriptions = '\n'.join(li_content)    
            if h2_tag and "Yêu cầu ứng viên" in h2_tag.text.strip():
                li_content = [li.text.strip() for li in div.find_all('li')]
                requirements = '\n'.join(li_content)

        job_data.append({
            'title': title,
            'company': company,
            'logo': logo,
            'url': job_url,
            'location': location,
            'salary': salary,
            'descriptions': descriptions,
            'requirements': requirements
        })

    return job_data