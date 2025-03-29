#!/bin/bash

# Start the PostgreSQL server in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
until pg_isready -h localhost -p 5432 -U $POSTGRES_USER; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run the Python script
python create_db.py --dbname "$POSTGRES_DB" --user "$POSTGRES_USER" --password "$POSTGRES_PASSWORD" --port 5432 --commands_file "ContainerDBScripts.sql"

# Keep the container running
tail -f /dev/null