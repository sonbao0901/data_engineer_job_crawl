CREATE DATABSE discord_bot_job
WITH
    OWNER = sonbao0901
    ENCODING = 'UTF8';

\c discord_bot_job

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE it_viec (
    
)