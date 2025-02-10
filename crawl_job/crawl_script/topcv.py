from bs4 import BeautifulSoup
from selenium import webdriver

def init_webdriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def scrape_jobs_topcv(url):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    jobs = soup.find_all('div', class_='job-item-search-result')

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
        driver = init_webdriver(job_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        divs = soup.find_all('div', class_='job-description__item')
        for div in divs:
            if "Mô tả công việc" in div.find('h3').text.strip():
                li_content = [li.text.strip() for li in div.find_all('li')]
                descriptions = '\n'.join(li_content)
            if "Yêu cầu ứng viên" in div.find('h3').text.strip():
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
        driver.quit()

    return job_data