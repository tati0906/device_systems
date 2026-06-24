from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse
)

from app.services.loan_service import (
    create_loan,
    get_loans,
    get_loan_by_id,
    get_loans_by_status,
    get_loans_by_device_type,
    get_loans_by_user,
    get_loans_by_device,
    return_loan
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.get(
    "/",
    response_model=list[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los préstamos",
    description="Consulta todos los préstamos registrados en el sistema."
)
def get_all_loans(
    db: Session = Depends(get_db)
):
    return get_loans(db)


@router.get(
    "/status/{returned}",
    response_model=list[LoanResponse],
    summary="Filtrar préstamos por estado"
)
def get_loans_status(
    returned: bool,
    db: Session = Depends(get_db)
):
    return get_loans_by_status(
        db,
        returned
    )


@router.get(
    "/device-type/{device_type}",
    response_model=list[LoanResponse],
    summary="Filtrar préstamos por tipo de dispositivo"
)
def get_loans_device_type(
    device_type: str,
    db: Session = Depends(get_db)
):
    return get_loans_by_device_type(
        db,
        device_type
    )


@router.get(
    "/user/{user_id}",
    response_model=list[LoanResponse],
    summary="Consultar préstamos de un usuario"
)
def get_user_loans(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_loans_by_user(
        db,
        user_id
    )


@router.get(
    "/device/{device_id}/history",
    response_model=list[LoanResponse],
    summary="Consultar historial de préstamos de un dispositivo"
)
def get_device_history(
    device_id: int,
    db: Session = Depends(get_db)
):
    return get_loans_by_device(
        db,
        device_id
    )


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo por ID"
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan = get_loan_by_id(
        db,
        loan_id
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado"
        )

    return loan


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo"
)
def create_new_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db)
):
    result = create_loan(
        db,
        loan
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if result == "device_not_found":
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    if result == "device_unavailable":
        raise HTTPException(
            status_code=409,
            detail="Dispositivo no disponible"
        )

    return result


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver dispositivo"
)
def return_device(
    loan_id: int,
    db: Session = Depends(get_db)
):
    result = return_loan(
        db,
        loan_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado"
        )

    if result == "already_returned":
        raise HTTPException(
            status_code=409,
            detail="El dispositivo ya fue devuelto"
        )

    return result