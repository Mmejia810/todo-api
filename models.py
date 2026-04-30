from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

from database import Base

class TareaDB(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, nullable=False)  # Agrega el campo id_user para relacionar con el usuario
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)


class usuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:     
        from_attributes = True  

class Usuariologin(BaseModel):
    email: str
    password: str

