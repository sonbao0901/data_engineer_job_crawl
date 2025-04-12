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