from db.resumen_estado_db import listar_documentos_usuario, definir_semaforo, agregar_doc_lista
from db.perfil_usuario_db import getUsuario
from db.perfil_usuario_db import persona
from db.perfil_usuario_db import getUsuario, updateUsuario, createUsuario
from db.supervision_db import Supervision
from db.supervision_db import getSupervision, updateSupervision
from modelos.perfil_usuario_modelo import personaIn, personaOut
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/resumen/{nombre}")
async def lista_doc_usuario(nombre: str):
    el_usuario = getUsuario(nombre)

    if el_usuario is None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")

    lista_doc = listar_documentos_usuario(nombre)
    if lista_doc is None:
        return {nombre: "No tiene documentos asignados"}

    for documento in lista_doc:
        definir_semaforo(documento)
    return lista_doc


@app.post("/cargar/documento")
async def agregar_doc(documento: DocumentoIn, nombre: str):
    if getUsuario(nombre) is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    definir_semaforo(documento)
    operacion_exitosa = agregar_doc_lista(documento, nombre)

    if operacion_exitosa:
        return operacion_exitosa
    else:
        return {documento: "Ya esta asignado a" + nombre}


# Operación GET (READ) para perfil de usuario

@app.get("/usuario/perfil/{usuario}")
async def get_Equipo(usuario: str):
    user = getUsuario(usuario)
    if user == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Mostrar si el usuario tiene un equipo a cargo
    equipo = getSupervision(usuario)
    if len(equipo) == 0:
        return {"Perfil": {"Usuario": user.idUsuario,
                           "Nombre": user.nombre,
                           "Apellido": user.apellido,
                           "Categoria": user.categoria,
                           "Equipo": "Nadie a cargo"}}

    return {"Perfil": {"Usuario": user.idUsuario,
                       "Nombre": user.nombre,
                       "Apellido": user.apellido,
                       "Categoria": user.categoria,
                       "Equipo": equipo}}


# Operación POST (CREATE) para perfil de usuario
@app.post("/usuario/perfil/")
async def crear_perfil_usuario(usuario: personaIn):

    usuario_db = getUsuario(usuario.idUsuario)

    if usuario_db == None:
        createUsuario(usuario)
    elif usuario_db != None:
        return {usuario: "Ya existe"}

    usuario_out = personaOut(**usuario_db.dict())
    return usuario_out

# Operación PUT (UPDATE) para perfil de usuario


@app.put("/usuario/perfil/")
async def modificar_perfil_usuario(usuario: personaIn):

    usuario_db = getUsuario(usuario.idUsuario)

    if usuario_db is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    updateUsuario(usuario_db)

    usuario_out = personaOut(**usuario_db.dict())
    return usuario_out
