from pydantic import BaseModel


class MainAlerts(BaseModel):
    gdac_id: str
    usgov_id: str
