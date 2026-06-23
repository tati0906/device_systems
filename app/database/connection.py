from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base de datos SQLite
DATABASE_URL = "sqlite:///./device_systems.db"

# Engine Crea la conexión con la base de datos.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()