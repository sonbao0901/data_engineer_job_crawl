#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for database..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 5
done
echo "Database is ready."

if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command -v python) -m pip install --upgrade pip
  $(command -v pip) install -r requirements.txt
fi

# Initialize the database
airflow db migrate

# Check if admin user exists
echo "Checking if admin user exists..."
ADMIN_EXISTS=$(airflow users list | grep -c "$AIRFLOW_USER" || true)
if [ "$ADMIN_EXISTS" -eq "0" ]; then
  echo "Creating admin user..."
  airflow users create \
    --username "$AIRFLOW_USER" \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password "$AIRFLOW_PASSWORD"
fi

exec airflow webserver