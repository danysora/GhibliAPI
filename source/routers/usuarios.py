from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..models import Usuario, ListaUsuarios, UsuarioActualizacion
from fastapi import Request

router = APIRouter()

@router.post("/usuarios", response_model=Usuario)
async def crear_usuario(usuario: Usuario, request: Request):
    usuario_dict = usuario.model_dump()
    result = request.app.state.database.usuarios.insert_one(usuario_dict)
    if result.acknowledged:
        usuario_dict["id"] = str(result.inserted_id)
        return Usuario(**usuario_dict)
    else:
        raise HTTPException(status_code=500, detail="Error al crear el usuario")

@router.get("/usuarios")
async def leer_usuarios(request: Request):
    usuarios = []
    for usuario in request.app.state.database.usuarios.find():
        usuarios.append(Usuario(id=str(usuario["_id"]), nombre=usuario["nombre"], rol=usuario["rol"]))
    return ListaUsuarios(usuarios=usuarios)

@router.get("/usuarios/{id}")
async def leer_usuario(id: str, request: Request):
    usuario = request.app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if usuario:
        return Usuario(id=str(usuario["_id"]), nombre=usuario["nombre"], rol=usuario["rol"])
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.put("/usuarios/{id}", response_model=Usuario, )
async def actualizar_usuario(id: str, usuario_actualizacion: UsuarioActualizacion, request: Request):
    usuario_existente = request.app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    actualizacion_data = usuario_actualizacion.model_dump(exclude_unset=True)

    if actualizacion_data:
        request.app.state.database.usuarios.update_one({'_id': ObjectId(id)}, {'$set': actualizacion_data})
        usuario_actualizado = request.app.state.database.usuarios.find_one({'_id': ObjectId(id)})
        return Usuario(id=str(usuario_actualizado["_id"]), nombre=usuario_actualizado["nombre"], rol=usuario_actualizado["rol"])
    else:
        return Usuario(id=str(usuario_existente["_id"]), nombre=usuario_existente["nombre"], rol=usuario_existente["rol"])
    
@router.delete("/usuarios/{id}")
async def borrar_usuario(id: str, request: Request):
    usuario_existente = request.app.state.database.usuarios.find_one({'_id': ObjectId(id)})
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    result = request.app.state.database.usuarios.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": f"Usuario con ID {id} borrado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al borrar el usuario")