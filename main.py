from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
#----------------------------
#conexion a la base de datos

#os.environ para despliegue. Descomente cuando ya probó todo local.


client = MongoClient(os.environ["MONGO_URI"])

#client = MongoClient("mongodb+srv://parranderos-user:87vYZqLNOSxGEwhf@fundamentosbd.1hqd9k3.mongodb.net/?appName=FundamentosBD")


#db = client["ISIS2304F19202610"] #base de datos 
db = client["parranderos"] #base de datos


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# Punto 6 - GET comentarios 
@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}, {"_id": 0}))
    return comentarios or {'mensaje': 'No se encontraron comentarios para este bar'}


# Punto 7 - POST comentarios (cambiar nombre de colección)
@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}


# Punto 8 - GET eventos
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find({"bar_id": bar_id}, {"_id": 0}))
    return eventos or {'mensaje': 'No se encontraron eventos para este bar'}#por si no ahy eventos 


# Punto 9 - POST eventos
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}