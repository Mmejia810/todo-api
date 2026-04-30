from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import models
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import SessionLocal

SECRET_KEY = "mi-clave-super-secreta-cambiala"
ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 30

# Le dices que use el algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])

def encriptar_password(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

def verificar_password(password, hash_guardado):
    return pwd_context.verify(password, hash_guardado)

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def leer_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = leer_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    usuario = db.query(models.usuarioDB).filter(models.usuarioDB.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    
    return usuario
    