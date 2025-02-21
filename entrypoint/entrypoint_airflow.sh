#!/bin/bash
set -e

# Wait for PostgreSQL using PGPASSWORD environment variable
while ! PGPASSWORD=$DB_PASSWORD psql -h postgres -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

# Initialize the database
airflow db init

# Create admin user if it doesn't exist
if ! airflow users list | grep -q "admin"; then
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
fi

# Start Airflow webserver
exec airflow webserver
