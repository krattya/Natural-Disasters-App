from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    MONGO_DATABASE_URI: str = "mongodb://root:example@mongo:27017"
    MONGO_DATABASE: str = "disaster_information"


settings = Settings()
