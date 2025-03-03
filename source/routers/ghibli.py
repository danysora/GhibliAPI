from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..models import Role, Usuario
import httpx
from fastapi import Request

router = APIRouter()

async def leer_usuario(id: str, request: Request):
    usuario = request.app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if usuario:
        return Usuario(id=str(usuario["_id"]), nombre=usuario["nombre"], rol=usuario["rol"])
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    
@router.get("/ghibli/{id}")
async def consultar_ghibli(id: str, consulta: str, request: Request):
    usuario = await leer_usuario(id, request)
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
    
@router.get("/ghibli/{id}/{objeto_id}")
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
