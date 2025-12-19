from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

app = FastAPI()

class MateriaCreate(BaseModel):
    nombre: str
    anio: int
    anual: bool
    cuatrimestre: Optional[int] = None
    correlativas: List[int] = Field(default_factory=list)

    @model_validator(mode= "after")
    def validar_cuatrimestre(materia):
        if materia.anual:
            materia.cuatrimestre = None
        else:
            if materia.cuatrimestre not in (1, 2):
                raise ValueError("Cuatrimestre invalido, debe ser 1 o 2")
        return materia

class MateriaResponse(BaseModel):
    id: int
    nombre: str
    anio: int
    modalidad: str
    correlativas: List[int]

class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    anio: Optional[int] = None
    anual: Optional[bool] = None
    cuatrimestre: Optional[int] = None
    correlativas: Optional[List[int]] = None

    @model_validator(mode= "after")
    def validar_cuatrimestre(materia):
        if materia.anual is None:
            return materia
        
        if materia.anual:
            materia.cuatrimestre = None
            return materia
        
        if materia.cuatrimestre not in (1, 2):
            raise ValueError("Cuatrimestre invalido, debe ser 1 o 2")
        
        return materia

def verify_modalidad (materia: MateriaCreate):
    if materia.anual:
        modalidad = "Anual"
    else:
        if materia.cuatrimestre not in (1, 2):
            raise ValueError("Cuatrimestre invalido, debe ser 1 o 2")

        modalidad = f"Cuatrimestre ({materia.cuatrimestre})"

    return modalidad

@app.get("/")
def root():
    return {"status": "ok"}

materias_db: List[MateriaResponse] = []
id_actual = 1

@app.post("/materias", response_model=MateriaResponse)
def agregar_mat(materia: MateriaCreate):
    global id_actual

    for mat in materias_db:
        if mat["nombre"].lower() == materia.nombre.lower():
            raise HTTPException(status_code=400, detail="La materia ya existe")

    modalidad = verify_modalidad(materia)

    nueva = {
        "id": int(id_actual),
        "nombre": materia.nombre,
        "anio": materia.anio,
        "modalidad": modalidad,
        "correlativas": materia.correlativas
    }

    materias_db.append(nueva)
    id_actual += 1

    return nueva

@app.get("/materias", response_model=List[MateriaResponse])
def get_materias():
    return materias_db

@app.get("/materias/{id}", response_model=MateriaResponse)
def get_mat(id: int):
    for materia in materias_db:
        if materia["id"] == id:
            return materia
        
    raise HTTPException(status_code=404,detail="No se pudo encontrar la materia")

@app.put("/materias/{id}", response_model=MateriaResponse)
def update_mat(id: int, materia: MateriaUpdate):

    materia_encontrada = None

    for mat in materias_db:
        if mat["id"] == id:
            materia_encontrada = mat
            break

    if materia_encontrada is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    if materia.nombre is not None:
        for mat1 in materias_db:
            if mat1["nombre"].lower() == materia.nombre.lower() and mat1["id"] != id:
                raise HTTPException(status_code=409, detail="No se puede tener 2 materias de mismo nombre")
            
        materia_encontrada["nombre"] = materia.nombre
    
    if materia.anio is not None:
        materia_encontrada["anio"] = materia.anio

    if materia.correlativas is not None:
        materia_encontrada["correlativas"] = materia.correlativas

    if materia.anual is not None or materia.cuatrimestre is not None:
        modalidad = verify_modalidad(materia)
        materia_encontrada["modalidad"] = modalidad

    return materia_encontrada

@app.delete("/materias/{id}", response_model=MateriaResponse)
def delete_mat(id: int):

    materia_encontrada = None

    for materia in materias_db:
        if materia["id"] == id:
            materia_encontrada = materia
            break
    
    if materia_encontrada is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    materias_db.remove(materia_encontrada)

    return materia_encontrada