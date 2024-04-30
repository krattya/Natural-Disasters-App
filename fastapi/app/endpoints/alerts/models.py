from pydantic import BaseModel, Field
from typing import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class AlertBase(BaseModel):
    title: str = Field(...)
