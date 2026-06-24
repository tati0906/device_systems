from datetime import datetime

from pydantic import BaseModel


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None = None
    returned: bool

    model_config = {
        "from_attributes": True
    }