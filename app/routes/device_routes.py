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

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Obtener todos los dispositivos",
    description="Consulta todos los dispositivos registrados en el sistema.",
    response_description="Lista de dispositivos obtenida correctamente."
)
def get_all_devices(
    db: Session = Depends(get_db)
):
    return get_devices(db)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
    description="Consulta un dispositivo específico mediante su identificador.",
    response_description="Información del dispositivo encontrada.",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = get_device_by_id(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo en el sistema.",
    response_description="Dispositivo creado correctamente."
)
def create_new_device(
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    return create_device(
        db,
        device
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente la información de un dispositivo.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def update_existing_device(
    device_id: int,
    device: DeviceUpdate,
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
    response_model=DeviceResponse,
    summary="Actualizar parcialmente dispositivo",
    description="Modifica uno o varios campos de un dispositivo.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def patch_existing_device(
    device_id: int,
    device: DevicePatch,
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
    "/{device_id}",
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo existente.",
    response_description="Dispositivo eliminado correctamente.",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def delete_existing_device(
    device_id: int,
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