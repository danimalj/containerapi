import psycopg2
import argparse

def execute_commands(db_params, commands_file):
    """
    Execute SQL commands from a configuration file using provided database parameters.
    """
    try:
        # Connect to the database using keyword arguments
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True  # Enable autocommit for commands like CREATE TABLESPACE
        cur = conn.cursor()

        # Read SQL commands from the configuration file
        with open(commands_file, "r") as file:
            commands = file.read().split(";")  # Split commands by semicolon

        # Execute each SQL command
        for command in commands:
            if command.strip():  # Skip empty commands
                try:
                    cur.execute(command)
                    print(f"Successfully executed:\n{command}")
                except Exception as e:
                    print(f"Error executing command:\n{command}\nError: {e}")

        # Close the cursor and connection
        cur.close()
        conn.close()
        print("All SQL commands executed successfully.")

    except Exception as e:
        print(f"Database connection failed. Error: {e}")

if __name__ == "__main__":
    # Use argparse to allow passing database parameters as keyword arguments
    parser = argparse.ArgumentParser(description="Run SQL commands with database parameters.")
    parser.add_argument("--dbname", required=True, help="Name of the PostgreSQL database")
    parser.add_argument("--user", required=True, help="Username for the PostgreSQL database")
    parser.add_argument("--password", required=True, help="Password for the PostgreSQL user")
    parser.add_argument("--host", default="localhost", help="Host of the PostgreSQL database")
    parser.add_argument("--port", default="5432", help="Port number for the PostgreSQL database")
    parser.add_argument("--commands_file", required=True, help="Path to the SQL commands configuration file")

    args = parser.parse_args()

    # Convert arguments to a dictionary to pass to psycopg2.connect
    db_params = {
        "dbname": args.dbname,
        "user": args.user,
        "password": args.password,
        "host": args.host,
        "port": args.port
    }

    execute_commands(db_params, args.commands_file)