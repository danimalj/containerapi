from fastapi import FastAPI
from app.routes import create_record, get_record, update_record, delete_record, container_info

app = FastAPI()

app.include_router(create_record.router)
app.include_router(get_record.router)
app.include_router(update_record.router)
app.include_router(delete_record.router)
app.include_router(container_info.router)