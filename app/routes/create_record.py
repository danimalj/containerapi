from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter()

# Define the request model for parsing JSON body
class Record(BaseModel):
    text: str

@router.post("/records")
async def create_record(record: Record):
    """
    Create a new record in the my_table:
    - Insert into text_field
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert record into my_table
        query = "INSERT INTO my_table (text_field) VALUES (%s) RETURNING id;"
        cursor.execute(query, (record.text,))
        new_record_id = cursor.fetchone()  # Assuming id is the primary key and auto-generated
        connection.commit()

        cursor.close()
        connection.close()

        return {"status": "success", "record_id": new_record_id}
    
    except Exception as e:
        error_message = f"Database error: {str(e)}"
        print(error_message)  # Debugging
        raise HTTPException(status_code=500, detail=error_message)