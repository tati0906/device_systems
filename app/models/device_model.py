from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    device_type = Column(String, nullable=False)
    available = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="device")