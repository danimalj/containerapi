from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db_connection

router = APIRouter()

class Record(BaseModel):
    text_field: str


@router.put("/records/{record_id}")
async def update_record(record_id: str, updated_text: str):
    """
    Update an existing record by its UUID.
    """
    try:
        # Connect to the database
        connection = get_db_connection()
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
        print(f"Updated record: {updated_record}")

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        if updated_record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"status": "success", "data": updated_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")