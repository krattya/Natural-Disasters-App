from fastapi import FastAPI
from app.endpoints.main import router
app = FastAPI()

app.include_router(router)

