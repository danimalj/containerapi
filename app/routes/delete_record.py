from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db_connection

router = APIRouter()

class Record(BaseModel):
    text_field: str

@router.delete("/records/delete/{record_id}")
async def delete_record(record_id: str):
    """
    Delete an existing record by its UUID.
    """
    try:
        connection = get_db_connection()
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