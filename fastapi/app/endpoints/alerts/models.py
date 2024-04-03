from pydantic import BaseModel, Field
from typing import Annotated, Optional
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class AlertBase(BaseModel):
    title: str = Field(...)


class AlertInDB(AlertBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
