from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware



import models
from database import engine, get_db
from auth import encriptar_password, verificar_password, crear_token, get_current_user

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tareas con Seguridad")

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---- MODELO PYDANTIC (Esquema de validación) ----
class TareaBase(BaseModel):
    titulo: str
    descripcion: str | None = None
    completada: bool = False

# ---- RUTAS ----

@app.get("/")
def inicio():
    return {"mensaje": "API de tareas funcionando correctamente"}

@app.post("/tareas", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaBase, db: Session = Depends(get_db), usuario_actual: models.usuarioDB = Depends(get_current_user)):
    nueva_tarea = models.TareaDB(
        id_user=usuario_actual.id,
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        completada=tarea.completada
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.get("/tareas")
def obtener_tareas(db: Session = Depends(get_db), usuario_actual: models.usuarioDB = Depends(get_current_user)):
    # Importante: Solo devolvemos las tareas del usuario autenticado
    return db.query(models.TareaDB).filter(models.TareaDB.id_user == usuario_actual.id).all()

@app.get("/tareas/{id}")
def obtener_tarea(id: int, db: Session = Depends(get_db), usuario_actual: models.usuarioDB = Depends(get_current_user)):
    tarea = db.query(models.TareaDB).filter(
        models.TareaDB.id == id, 
        models.TareaDB.id_user == usuario_actual.id
    ).first()
    
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.put("/tareas/{id}")
def actualizar_tarea(id: int, tarea_actualizada: TareaBase, db: Session = Depends(get_db), usuario_actual: models.usuarioDB = Depends(get_current_user)):
    tarea = db.query(models.TareaDB).filter(
        models.TareaDB.id == id, 
        models.TareaDB.id_user == usuario_actual.id
    ).first()
    
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    tarea.titulo = tarea_actualizada.titulo
    tarea.descripcion = tarea_actualizada.descripcion
    tarea.completada = tarea_actualizada.completada
    
    db.commit()
    db.refresh(tarea)
    return tarea

@app.delete("/tareas/{id}")
def eliminar_tarea(id: int, db: Session = Depends(get_db), usuario_actual: models.usuarioDB = Depends(get_current_user)):
    tarea = db.query(models.TareaDB).filter(
        models.TareaDB.id == id, 
        models.TareaDB.id_user == usuario_actual.id
    ).first()
    
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(tarea)
    db.commit()
    return {"mensaje": f"Tarea {id} eliminada correctamente"}

# ---- RUTAS DE AUTENTICACIÓN ----

@app.post("/Registrar", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: models.UsuarioCreate, db: Session = Depends(get_db)):
    existente_usuario = db.query(models.usuarioDB).filter(models.usuarioDB.email == usuario.email).first()
    if existente_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_pw = encriptar_password(usuario.password)
    nuevo_usuario = models.usuarioDB(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hashed_pw
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email
    }

@app.post("/Login")
def login_usuario(usuario: models.Usuariologin, db: Session = Depends(get_db)):
    usuario_db = db.query(models.usuarioDB).filter(models.usuarioDB.email == usuario.email).first()
    
    if not usuario_db or not verificar_password(usuario.password, usuario_db.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = crear_token({"sub": usuario_db.email})
    return {"access_token": token, "token_type": "bearer"}