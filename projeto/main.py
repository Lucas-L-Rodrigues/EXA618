from fastapi import FastAPI
import json
import math
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#################################################################################
# Carregamento dos dados
#################################################################################

# Usando um 'truque' para pegar o caminho do arquivo,
# pois pegando normalmente tive problemas com o caminho relativo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(BASE_DIR, "data", "bares.json")

with open(caminho_arquivo, "r", encoding="utf-8") as f:
    data = json.load(f)

# Puxando os bares do arquivo para memória
bares = data["features"]

# Armazenamento de likes em memória
# chave = id do bar
# valor = quantidade de likes
likes = {}

# Formula de Haversine para determinar a distância entre 2 pontos em uma esfera:
# distância = 2 * R * arcsin(sqrt(sin²((lat2 - lat1)/2) + cos(lat1) * cos(lat2) * sin²((lon2 - lon1)/2)))
# OBS: Apesar da fórmula ser grande não foi tão difícil quanto eu esperava

def calcular_distancia(lat1, lon1, lat2, lon2):

    r = 6371  # raio da Terra em km

    # distância entre as latitudes e longitudes
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # parte interna da fórmula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    distancia = r * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return distancia

#################################################################################
# Endpoints
#################################################################################

# Botei aqui só pra testar se a API tava funcionando no começo do projeto
@app.get("/")
def home():
    return {
        "mensagem": "A API está funcionando"
    }


#################################################################################
# Listagem completa de bares
#################################################################################

@app.get("/bares")
def listar_bares():

    resultado = []

    for indice, bar in enumerate(bares):

        lon_bar, lat_bar = bar["geometry"]["coordinates"]

        resultado.append({
            "id": indice,
            "nome": bar["properties"]["nome"],
            "endereco": bar["properties"]["endereco"],
            "latitude": lat_bar,
            "longitude": lon_bar,
            "likes": likes.get(indice, 0)
        })

    return resultado


#################################################################################
# Busca por raio
#################################################################################

@app.get("/bares/proximos")
def bares_proximos(
    lat: float,
    lon: float,
    raio_km: float
):

    resultado = []

    for indice, bar in enumerate(bares):

        lon_bar, lat_bar = bar["geometry"]["coordinates"]

        distancia = calcular_distancia(
            lat,
            lon,
            lat_bar,
            lon_bar
        )

        if distancia <= raio_km:

            resultado.append({
                "id": indice,
                "nome": bar["properties"]["nome"],
                "endereco": bar["properties"]["endereco"],
                "latitude": lat_bar,
                "longitude": lon_bar,
                "distancia_km": round(distancia, 3),
                "likes": likes.get(indice, 0)
            })

    return resultado


#################################################################################
# 10 bares mais próximos
#################################################################################

@app.get("/bares/mais-proximos")
def bares_mais_proximos(
    lat: float,
    lon: float
):

    resultado = []

    for indice, bar in enumerate(bares):

        lon_bar, lat_bar = bar["geometry"]["coordinates"]

        distancia = calcular_distancia(
            lat,
            lon,
            lat_bar,
            lon_bar
        )

        resultado.append({
            "id": indice,
            "nome": bar["properties"]["nome"],
            "endereco": bar["properties"]["endereco"],
            "latitude": lat_bar,
            "longitude": lon_bar,
            "distancia_km": round(distancia, 3),
            "likes": likes.get(indice, 0)
        })

    resultado.sort(
        key=lambda bar: bar["distancia_km"]
    )

    return resultado[:10]


#################################################################################
# Dar like
#################################################################################

@app.post("/bares/{bar_id}/like")
def curtir_bar(bar_id: int):

    if bar_id < 0 or bar_id >= len(bares):
        return {
            "erro": "Bar não encontrado"
        }

    likes[bar_id] = likes.get(bar_id, 0) + 1

    return {
        "mensagem": "Like registrado com sucesso",
        "bar_id": bar_id,
        "likes": likes[bar_id]
    }


#################################################################################
# Consultar likes
#################################################################################

@app.get("/bares/{bar_id}/likes")
def consultar_likes(bar_id: int):

    if bar_id < 0 or bar_id >= len(bares):
        return {
            "erro": "Bar não encontrado"
        }

    return {
        "bar_id": bar_id,
        "likes": likes.get(bar_id, 0)
    }


