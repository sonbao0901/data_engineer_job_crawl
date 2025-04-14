CREATE TABLE IF NOT EXISTS bronze.topcv_data_job (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(150) NOT NULL,
    logo TEXT, 
    url TEXT UNIQUE, 
    location VARCHAR(100), 
    salary VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bronze.itviec_data_job (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(150) NOT NULL,
    logo TEXT, 
    url TEXT UNIQUE, 
    location VARCHAR(100), 
    mode VARCHAR(50),
    tags VARCHAR(200),
    descriptions TEXT, 
    requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add new columns to bronze.itviec_data_job
alter table bronze.topcv_data_job
add column descriptions text,
add column requirements text,
add column experience varchar(100),
add column education varchar(100),
add column type_of_work varchar(50);
-- DDL
-- TRUNCATE TABLE discord_job_db.bronze.itviec_data_job;
-- TRUNCATE TABLE discord_job_db.bronze.topcv_data_job;
-- ALTER SEQUENCE discord_job_db.bronze.topcv_data_job_id_seq RESTART WITH 1;
-- ALTER SEQUENCE discord_job_db.bronze.itviec_data_job_id_seq RESTART WITH 1;