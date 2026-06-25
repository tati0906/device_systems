from datetime import datetime

from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device

from app.schemas.loan_schema import LoanCreate


def create_loan(
    db: Session,
    loan_data: LoanCreate
):
    user = (
        db.query(User)
        .filter(User.id == loan_data.user_id)
        .first()
    )

    if not user:
        return None

    device = (
        db.query(Device)
        .filter(Device.id == loan_data.device_id)
        .first()
    )

    if not device:
        return "device_not_found"

    if not device.available:
        return "device_unavailable"

    loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id
    )

    device.available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def get_loans(db: Session):
    return db.query(Loan).all()


def get_loan_by_id(
    db: Session,
    loan_id: int
):
    return (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )


def get_loans_by_status(
    db: Session,
    returned: bool
):
    return (
        db.query(Loan)
        .filter(Loan.returned == returned)
        .all()
    )


def get_loans_by_device_type(
    db: Session,
    device_type: str
):
    return (
        db.query(Loan)
        .join(Device)
        .filter(Device.device_type == device_type)
        .all()
    )


def get_loans_by_user(
    db: Session,
    user_id: int
):
    return (
        db.query(Loan)
        .filter(Loan.user_id == user_id)
        .all()
    )


def get_loans_by_device(
    db: Session,
    device_id: int
):
    return (
        db.query(Loan)
        .filter(Loan.device_id == device_id)
        .all()
    )


def return_loan(
    db: Session,
    loan_id: int
):
    loan = get_loan_by_id(
        db,
        loan_id
    )

    if not loan:
        return None

    if loan.returned:
        return "already_returned"

    loan.returned = True

    loan.return_date = datetime.utcnow()

    device = (
        db.query(Device)
        .filter(Device.id == loan.device_id)
        .first()
    )

    if device:
        device.available = True

    db.commit()
    db.refresh(loan)

    return loan

def get_loan_details(db: Session):
    return db.query(Loan).all()