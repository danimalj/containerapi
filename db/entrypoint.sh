#!/bin/bash

# Start the PostgreSQL server in the background
#docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
#echo "Waiting for PostgreSQL to start..."
#until pg_isready -h localhost -p 5432 -U $POSTGRES_USER; do
#  sleep 1
#done
#echo "PostgreSQL is ready!"

# Run the Python script
#python create_db.py --dbname "$POSTGRES_DB" --user "$POSTGRES_USER" --password "$POSTGRES_PASSWORD" --port 5432 --commands_file "ContainerDBScripts.sql"

# Keep the container running
#tail -f /dev/null
#!/bin/bash

# Start the PostgreSQL server in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done
echo "PostgreSQL is ready!"
sleep 5
# Execute the SQL script through PostgreSQL
echo "Running create_tablespace.sql..."
psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/app/create_tablespace.sql"
echo "SQL create_tablespace.sql script executed successfully!"
sleep 5
echo "Running create_my_table.sql..."
psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/app/create_my_table.sql"
echo "SQL ContainerDBCreateScript.sql script executed successfully!"
sleep 5
echo "Running create_modify_trigger_function.sql..."
psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/app/create_modify_trigger_function.sql"
echo "SQL create_modify_trigger_function.sql script executed successfully!"
sleep 5
echo "Running create_trigger.sql..."
psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/app/create_trigger.sql"
echo "SQL create_trigger.sql script executed successfully!"
sleep 5
echo "Running create_users.sql..."
psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/app/create_users.sql"
echo "SQL create_users.sql script executed successfully!"

# Keep the container running
tail -f /dev/null