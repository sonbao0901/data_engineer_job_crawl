CREATE DATABSE discord_bot_job
WITH
    OWNER = sonbao0901
    ENCODING = 'UTF8';

\c discord_bot_job

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE it_viec (
    title TEXT,
    company TEXT,
    logo TEXT,
    url TEXT UNIQUE,
    location TEXT,
    mode TEXT,
    tags TEXT,
    descriptions TEXT,
    requirements TEXT
)

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