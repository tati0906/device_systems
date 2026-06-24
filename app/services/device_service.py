from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch
)


def create_device(db: Session, device: DeviceCreate):

    existing_device = (
        db.query(Device)
        .filter(Device.serial_number == device.serial_number)
        .first()
    )

    if existing_device:
        raise HTTPException(
            status_code=400,
            detail="El serial ya está registrado"
        )

    new_device = Device(**device.model_dump())

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device


def get_devices(db: Session):
    return db.query(Device).all()


def get_device_by_id(db: Session, device_id: int):
    return (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )


def update_device(
    db: Session,
    device_id: int,
    device_data: DeviceUpdate
):
    device = get_device_by_id(db, device_id)

    if not device:
        return None

    existing_device = (
        db.query(Device)
        .filter(
            Device.serial_number == device_data.serial_number,
            Device.id != device_id
        )
        .first()
    )

    if existing_device:
        raise HTTPException(
            status_code=400,
            detail="El serial ya está registrado"
        )

    data = device_data.model_dump()

    for key, value in data.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return device


def patch_device(
    db: Session,
    device_id: int,
    device_data: DevicePatch
):
    device = get_device_by_id(db, device_id)

    if not device:
        return None

    data = device_data.model_dump(
        exclude_unset=True
    )

    if "serial_number" in data:

        existing_device = (
            db.query(Device)
            .filter(
                Device.serial_number == data["serial_number"],
                Device.id != device_id
            )
            .first()
        )

        if existing_device:
            raise HTTPException(
                status_code=400,
                detail="El serial ya está registrado"
            )

    for key, value in data.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return device


def delete_device(
    db: Session,
    device_id: int
):
    device = get_device_by_id(db, device_id)

    if not device:
        return None

    db.delete(device)
    db.commit()

    return device