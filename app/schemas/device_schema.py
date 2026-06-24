from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=3)
    serial_number: str = Field(..., min_length=3)
    device_type: str = Field(..., min_length=3)


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=3)
    serial_number: str = Field(..., min_length=3)
    device_type: str = Field(..., min_length=3)
    available: bool


class DevicePatch(BaseModel):
    name: str | None = None
    serial_number: str | None = None
    device_type: str | None = None
    available: bool | None = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    available: bool

    model_config = {
        "from_attributes": True
    }