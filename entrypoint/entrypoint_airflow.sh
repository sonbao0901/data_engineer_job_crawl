#!/bin/bash

echo "Starting Airflow set up..."

airflow db init

USER_EXISTS=$(airflow users list | grep -c "admin")

if [ "$USER_EXISTS" -eq 0 ]; then
    airflow users create \
        --username sonbao \
        --password thongminh \
        --firstname Bao \
        --lastname Phan \
        --role Admin \
        --email phanb688@gmail.com
fi

exec airflow webserver