from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from bson import ObjectId
import httpx
import contextlib

class Role(str, Enum):
    admin = "admin"
    films = "films"
    people = "people"
    locations = "locations"
    species = "species"
    vehicles = "vehicles"

class Usuario(BaseModel):
    nombre: str
    rol: Role
    id: Optional[str] = None
usuarios = []

class ListaUsuarios(BaseModel):
    usuarios: List[Usuario]
    
class UsuarioActualizacion(BaseModel):
    nombre: Optional[str] = None
    rol: Optional[Role] = None
    
    
MONGO_URI = "mongodb://localhost/pythonmongodb"

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = MongoClient(MONGO_URI)
    app.state.database = app.state.mongo_client.get_database()
    yield
    app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)


@app.post("/usuarios", response_model=Usuario)
async def crear_usuario(usuario: Usuario):
    usuario_dict = usuario.model_dump()
    result = app.state.database.usuarios.insert_one(usuario_dict)
    if result.acknowledged:
        usuario_dict["id"] = str(result.inserted_id)
        return Usuario(**usuario_dict)
    else:
        raise HTTPException(status_code=500, detail="Error al crear el usuario")

@app.get("/usuarios")
async def leer_usuarios():
    usuarios = []
    for usuario in app.state.database.usuarios.find():
        usuarios.append(Usuario(id=str(usuario["_id"]), nombre=usuario["nombre"], rol=usuario["rol"]))
    return ListaUsuarios(usuarios=usuarios)

@app.get("/usuarios/{id}")
async def leer_usuario(id: str):
    usuario = app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if usuario:
        return Usuario(id=str(usuario["_id"]), nombre=usuario["nombre"], rol=usuario["rol"])
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.put("/usuarios/{id}", response_model=Usuario)
async def actualizar_usuario(id: str, usuario_actualizacion: UsuarioActualizacion):
    usuario_existente = app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    actualizacion_data = usuario_actualizacion.model_dump(exclude_unset=True)

    if actualizacion_data:
        app.state.database.usuarios.update_one({'_id': ObjectId(id)}, {'$set': actualizacion_data})
        usuario_actualizado = app.state.database.usuarios.find_one({'_id': ObjectId(id)})
        return Usuario(id=str(usuario_actualizado["_id"]), nombre=usuario_actualizado["nombre"], rol=usuario_actualizado["rol"])
    else:
        return Usuario(id=str(usuario_existente["_id"]), nombre=usuario_existente["nombre"], rol=usuario_existente["rol"])
    
@app.delete("/usuarios/{id}")
async def borrar_usuario(id: str):
    usuario_existente = app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    result = app.state.database.usuarios.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": f"Usuario con ID {id} borrado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al borrar el usuario")
    
@app.get("/ghibli/{id}")
async def consultar_ghibli(id: str, consulta: str):
    usuario = await leer_usuario(id)
    rol_usuario = usuario.rol

    if rol_usuario == Role.admin or rol_usuario.value == consulta:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ghibliapi.vercel.app/{consulta}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error al consultar la API de Ghibli")
    else:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
    
@app.get("/ghibli/{id}/{objeto_id}")
async def consultar_uno_ghibli(id: str, consulta: str, objeto_id: str):
    usuario = await leer_usuario(id)
    rol_usuario = usuario.rol

    if rol_usuario == Role.admin or rol_usuario.value == consulta:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ghibliapi.vercel.app/{consulta}/{objeto_id}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Objeto no encontrado o error en la API de Ghibli")
    else:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
