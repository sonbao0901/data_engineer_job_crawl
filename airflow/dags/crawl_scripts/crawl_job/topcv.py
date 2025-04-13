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
        descriptions = ''
        requirements = ''
        descriptions = ''
        requirements = ''
        exp = ''
        edu = ''
        type_of_work = ''
        # Check if the job title contains any of the keywords
        driver = init_webdriver(job_url)
        time.sleep(2)
        page_source = driver.page_source
        time.sleep(2)
        soup = BeautifulSoup(page_source, "html.parser")
        divs = soup.find_all('div', class_='box-info') or soup.find_all('div', class_='premium-job-description__box')
        driver.quit()

        if job_url.startswith('https://www.topcv.vn/brand'):
            for div in divs:
                h2_tag = div.find('h2', class_="title")
                if h2_tag and "Mô tả công việc" in h2_tag.text.strip():
                    descriptions = div.find('div', class_='content-tab').text.strip()
                if h2_tag and "Yêu cầu ứng viên" in h2_tag.text.strip():
                    requirements = div.find('div', class_='content-tab').text.strip()
                if h2_tag and "Thông tin" in h2_tag.text.strip():
                    box_items = div.find_all('div', class_='box-item')
                    for item in box_items:
                        strong_tag = item.find('strong')
                        span_tag = item.find('span')
                        if strong_tag and span_tag:
                            label = strong_tag.text.strip()
                            value = span_tag.text.strip()
                            if label == "Kinh nghiệm":
                                exp = value
                            elif label == "Học vấn":
                                edu = value
                            elif label == "Hình thức làm việc":
                                type_of_work = value

        if job_url.startswith('https://www.topcv.vn/viec-lam'):
            
            divs = soup.find_all('div', class_='job-description__item')
            for div in divs:
                h3_tag = div.find("h3").get_text(strip=True)
                if "Mô tả công việc"== h3_tag:
                    descriptions = div.find('div', class_='job-description__item--content').text.strip()
                if "Yêu cầu ứng viên"==h3_tag:
                    requirements = div.find('div', class_='job-description__item--content').text.strip()
                
            exp_divs = soup.find_all('div', class_='job-detail__info--section-content-value')
            exp = exp_divs[-1].text

            divs = soup.find_all('div', class_='box-general-group')
            for div in divs:

                div_identifier = div.find('div', class_='box-general-group-info-title').text
                if "Hình thức làm việc"==div_identifier:
                    type_of_work = div.find('div', class_='box-general-group-info-value').text.strip()
                if "Học vấn"==div_identifier:
                    edu = div.find('div', class_='box-general-group-info-value').text.strip()
            

        job_data.append({
            'title': title,
            'company': company,
            'logo': logo,
            'url': job_url,
            'location': location,
            'salary': salary,
            'descriptions': descriptions,
            'requirements': requirements,
            'experience': exp,
            'education': edu,
            'type_of_work': type_of_work
        })

    return job_data