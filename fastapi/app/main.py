from fastapi import FastAPI
from app.endpoints.main import router as main_router
from app.core.config import settings
from pymongo import MongoClient


app = FastAPI(
    title="Disaster Information API", description="API for disaster information"
)
# Connect to mongo db

client = MongoClient(settings.MONGO_DATABASE_URI)
db = client.get_database(settings.MONGO_DATABASE)
app.db = db
app.include_router(main_router, prefix=settings.API_V1_STR)
