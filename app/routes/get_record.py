from fastapi import APIRouter, HTTPException, Query
from app.database import get_db_connection

router = APIRouter()

@router.get("/records")
async def get_data(record_id: str = None, records: int = None):
    """
    Retrieve data based on the specified query parameters:
    - Summary of records grouped by `updated_by`
    - A single record by UUID
    - A list of records (limit specified)
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if record_id:
            # Retrieve a single record by UUID
            query = "SELECT * FROM my_table WHERE id = %s;"
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()

            if record is None:
                raise HTTPException(status_code=404, detail="Record not found")
            return {"status": "success", "data": record}

        elif records:
            # Retrieve a limited list of records ordered by creation date
            query = "SELECT * FROM my_table ORDER BY created_at DESC LIMIT %s;"
            cursor.execute(query, (records,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            return {"status": "success", "data": data}

        else:
            # Retrieve a summary grouped by `updated_by`
            query = "SELECT updated_by, count(1) AS summary FROM my_table GROUP BY updated_by;"
            cursor.execute(query)
            summary = cursor.fetchall()
            print("Query result:", summary)  # Debugging
            cursor.close()
            connection.close()

            if not summary:
                raise HTTPException(status_code=404, detail="No summary data found")

            try:
                # Process and return the summary results
                return {
                    "status": "success",
                    "data": [{"updated_by": row["updated_by"], "count": row["summary"]} for row in summary]
                }
            except Exception as e:
                # Handle errors during response construction
                error_message = f"Database error during response construction: {str(e)}"
                print(error_message)  # Debugging
                raise HTTPException(status_code=500, detail=error_message)

    except Exception as e:
        # General error handling for database connection or query execution
        error_message = f"Database error: {str(e)}"
        print(error_message)  # Debugging
        raise HTTPException(status_code=500, detail=error_message)