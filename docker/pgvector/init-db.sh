#!/bin/bash
echo "Running InitDB"
set -e

# Function to check if a user exists
user_exists() {
    psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$1'" | grep -q 1
}

# Function to check if a database exists
database_exists() {
    psql -tAc "SELECT 1 FROM pg_database WHERE datname='$1'" | grep -q 1
}

# Connect to PostgreSQL and install the pgvector extension
# Note: This command is commented out, you may uncomment it if needed
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
#     CREATE EXTENSION IF NOT EXISTS vector;
# EOSQL

# Check if user exists, if not create it
if user_exists "$POSTGRES_USER"; then
  echo "User $POSTGRES_USER already exists."
else
  psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE USER "$POSTGRES_USER" WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';
EOSQL
  echo "User $POSTGRES_USER created."
fi

# Check if database exists, if not create it
if database_exists "$POSTGRES_DB"; then
  echo "Database $POSTGRES_DB already exists."
else
  psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE DATABASE "$POSTGRES_DB";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL
  echo "Database $POSTGRES_DB created."
fi

# Connect to the database to install extensions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL
echo "Extension vector created in database $POSTGRES_DB."