#!/bin/bash
# Remove the source .env line
set -e

# Wait for the database to be ready
echo "Waiting for database..."
until pg_isready -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
  sleep 5
done
echo "Database is ready."

if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command python) pip install --upgrade pip
  $(command -v pip) install -r requirements.txt  # Removed --user flag
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username ${AIRFLOW_USER} \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password ${AIRFLOW_PASSWORD}
fi

$(command -v airflow) db upgrade

exec airflow webserver