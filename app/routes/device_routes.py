from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch,
    DeviceResponse
)

from app.services.device_service import (
    create_device,
    get_devices,
    get_device_by_id,
    update_device,
    patch_device,
    delete_device
)

from app.dependencies.auth_dependency import (
    require_admin,
    require_admin_or_support
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=list[DeviceResponse]
)
def get_all_devices(
    db: Session = Depends(get_db)
):
    return get_devices(db)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = get_device_by_id(db, device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201
)
def create_new_device(
    device: DeviceCreate,
    current_user=Depends(require_admin_or_support),
    db: Session = Depends(get_db)
):
    return create_device(db, device)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse
)
def update_existing_device(
    device_id: int,
    device: DeviceUpdate,
    current_user=Depends(require_admin_or_support),
    db: Session = Depends(get_db)
):
    updated = update_device(
        db,
        device_id,
        device
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return updated


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse
)
def patch_existing_device(
    device_id: int,
    device: DevicePatch,
    current_user=Depends(require_admin_or_support),
    db: Session = Depends(get_db)
):
    updated = patch_device(
        db,
        device_id,
        device
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return updated


@router.delete(
    "/{device_id}"
)
def delete_existing_device(
    device_id: int,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    deleted = delete_device(
        db,
        device_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return {
        "message": "Dispositivo eliminado"
    }

