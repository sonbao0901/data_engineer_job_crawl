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

def extract_job_info(job):
    title = job.find('h3').text.strip()
    company = job.find('a', class_='company').text.strip()
    
    img_tag = job.find('img')
    logo = img_tag.get('src') or img_tag.get('data-src', '')

    job_url = job.find('a')['href']
    location = job.find('label', class_='address').text.strip()
    salary = job.find('label', class_='title-salary').text.strip()

    return title, company, logo, job_url, location, salary

def parse_brand_job(soup):
    descriptions = requirements = exp = edu = type_of_work = ''
    divs = soup.find_all('div', class_='box-info') or soup.find_all('div', class_='premium-job-description__box')
    
    for div in divs:
        h2_tag = div.find('h2', class_="title")
        if not h2_tag:
            continue

        title_text = h2_tag.text.strip()
        content = div.find('div', class_='content-tab')
        if "Mô tả công việc" in title_text:
            descriptions = content.text.strip() if content else ''
        elif "Yêu cầu ứng viên" in title_text:
            requirements = content.text.strip() if content else ''
        elif "Thông tin" in title_text:
            for item in div.find_all('div', class_='box-item'):
                strong = item.find('strong')
                span = item.find('span')
                if strong and span:
                    label = strong.text.strip()
                    value = span.text.strip()
                    if label == "Kinh nghiệm":
                        exp = value
                    elif label == "Học vấn":
                        edu = value
                    elif label == "Hình thức làm việc":
                        type_of_work = value
    return descriptions, requirements, exp, edu, type_of_work

def parse_job_detail(soup):
    descriptions = requirements = exp = edu = type_of_work = ''

    for div in soup.find_all('div', class_='job-description__item'):
        h3_tag = div.find("h3")
        content = div.find('div', class_='job-description__item--content')
        if h3_tag and content:
            title = h3_tag.get_text(strip=True)
            if title == "Mô tả công việc":
                descriptions = content.text.strip()
            elif title == "Yêu cầu ứng viên":
                requirements = content.text.strip()

    exp_divs = soup.find_all('div', class_='job-detail__info--section-content-value')
    if exp_divs:
        exp = exp_divs[-1].text.strip()

    for div in soup.find_all('div', class_='box-general-group'):
        title_div = div.find('div', class_='box-general-group-info-title')
        value_div = div.find('div', class_='box-general-group-info-value')
        if title_div and value_div:
            label = title_div.text.strip()
            value = value_div.text.strip()
            if label == "Hình thức làm việc":
                type_of_work = value
            elif label == "Học vấn":
                edu = value

    return descriptions, requirements, exp, edu, type_of_work

def scrape_jobs_topcv(url):
    driver = init_webdriver(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    time.sleep(5)
    jobs = soup.find_all('div', class_='job-item-search-result')
    driver.quit()

    job_data = []

    for job in jobs:
        title, company, logo, job_url, location, salary = extract_job_info(job)

        driver = init_webdriver(job_url)
        job_soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(5)
        driver.quit()

        if job_url.startswith('https://www.topcv.vn/brand'):
            descriptions, requirements, exp, edu, type_of_work = parse_brand_job(job_soup)
        elif job_url.startswith('https://www.topcv.vn/viec-lam'):
            descriptions, requirements, exp, edu, type_of_work = parse_job_detail(job_soup)
        else:
            descriptions = requirements = exp = edu = type_of_work = ''

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