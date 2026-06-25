from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin,
    require_admin_or_support
)

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

from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.get(
    "/",
    response_model=list[LoanResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)]
)
def get_all_loans(
    db: Session = Depends(get_db)
):
    return get_loans(db)


@router.get(
    "/details",
    dependencies=[Depends(require_admin_or_support)]
)
def get_loan_details(
    db: Session = Depends(get_db)
):
    return get_loans(db)


@router.get(
    "/status/{returned}",
    response_model=list[LoanResponse]
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
    response_model=list[LoanResponse]
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
    response_model=list[LoanResponse]
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
    response_model=list[LoanResponse]
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
    status_code=status.HTTP_200_OK
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
    dependencies=[Depends(get_current_active_user)]
)
@limiter.limit("10/minute")
def create_new_loan(
    request: Request,
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
    dependencies=[Depends(require_admin_or_support)]
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

