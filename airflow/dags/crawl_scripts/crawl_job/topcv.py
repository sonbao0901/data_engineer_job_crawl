import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def init_webdriver(url):
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
        
        # # Initialize descriptions and requirements with default values
        # descriptions = ''
        # requirements = ''
        
        # driver = init_webdriver(job_url)
        # time.sleep(3)
        # page_source = driver.page_source
        # soup = BeautifulSoup(page_source, "html.parser")
        # divs = soup.find_all('div', class_='box-info')
        # driver.quit()

        # for div in divs:
        #     h2_tag = div.find('h2', class_="title")     
        #     if h2_tag and "Mô tả công việc" in h2_tag.text.strip():
        #         div.find('div', class_=)
        #         li_content = [li.text.strip() for li in div.find_all('li')]
        #         descriptions = '\n'.join(li_content)
        #         break   
        #     if h2_tag and "Yêu cầu ứng viên" in h2_tag.text.strip():
        #         li_content = [li.text.strip() for li in div.find_all('li')]
        #         requirements = '\n'.join(li_content)
        #         break
        job_data.append({
            'title': title,
            'company': company,
            'logo': logo,
            'url': job_url,
            'location': location,
            'salary': salary
        })

    return job_data