from pydantic import BaseModel,EmailStr
from datetime import date
from warehouse.enums import CampaignsStatus,CustomerStatus
from typing import Any

class CustomerSchema(BaseModel):
    id : int
    name : str
    email : EmailStr
    status : CustomerStatus
    createdTime : date

    class Config:
        from_attributes = True

class CampaignsSchema(BaseModel):
    id : int
    name : str
    budget : int
    status : CampaignsStatus
    startDate : date
    endDate : date

    class Config:
        from_attributes = True

class TaskStatus(BaseModel):
    id: str
    status: str
    result: Any = None

class WebhookPayload(BaseModel):
    event_type: str
    data: dict


