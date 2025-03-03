from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

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

class ListaUsuarios(BaseModel):
    usuarios: List[Usuario]

class UsuarioActualizacion(BaseModel):
    nombre: Optional[str] = None
    rol: Optional[Role] = None