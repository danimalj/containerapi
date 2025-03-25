from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Define the FastAPI app
app = FastAPI()

# Database connection settings
DB_SETTINGS = {
    "host": "db",  # The Docker service name of the PostgreSQL container
    "port": 5432,
    "database": "dockdbtest",
    "user": "admin",
    "password": "admin",
}

# Request model for inserting data
class Record(BaseModel):
    text_field: str

# Endpoint to insert a new record
@app.post("/records/")
async def create_record(record: Record):
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)
        cursor = connection.cursor()

        # Insert record into the database
        insert_query = """
            INSERT INTO my_table (text_field) VALUES (%s)
            RETURNING id, text_field, created_at;
        """
        cursor.execute(insert_query, (record.text_field,))
        new_record = cursor.fetchone()

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        return {"status": "success", "data": new_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    from typing import List, Optional

@app.get("/records/{record_id}")
async def get_record(record_id: str):
    """
    Retrieve a single record by its UUID (id).
    """
    try:
        connection = psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)
        cursor = connection.cursor()

        query = "SELECT * FROM my_table WHERE id = %s;"
        cursor.execute(query, (record_id,))
        record = cursor.fetchone()

        cursor.close()
        connection.close()

        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"status": "success", "data": record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/records/")
async def get_last_100_records():
    """
    Retrieve the last 100 transactions.
    """
    try:
        connection = psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)
        cursor = connection.cursor()

        query = "SELECT * FROM my_table ORDER BY created_at DESC LIMIT 100;"
        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"status": "success", "data": records}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
from typing import Optional

@app.put("/records/{record_id}")
async def update_record(record_id: str, updated_text: str):
    """
    Update an existing record by its UUID.
    """
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)
        cursor = connection.cursor()

        # Update the record in the database
        update_query = """
            UPDATE my_table
            SET text_field = %s, updated_at = current_timestamp, updated_by = current_user
            WHERE id = %s
            RETURNING id, text_field, updated_at, updated_by;
        """
        cursor.execute(update_query, (updated_text, record_id))
        updated_record = cursor.fetchone()

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        if updated_record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"status": "success", "data": updated_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.delete("/records/{record_id}")
async def delete_record(record_id: str):
    """
    Delete an existing record by its UUID.
    """
    try:
        connection = psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)
        cursor = connection.cursor()

        delete_query = "DELETE FROM my_table WHERE id = %s RETURNING id, text_field;"
        cursor.execute(delete_query, (record_id,))
        deleted_record = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        if deleted_record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"status": "success", "data": deleted_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")