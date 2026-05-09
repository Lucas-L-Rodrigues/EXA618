from fastapi import FastAPI
import json
import math
import os # Usando para pegar o diretório

app = FastAPI()

# Usando um 'truque' para pegar o caminho do arquivo, pois pegando normalmente tive problemas com o caminho relativo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(BASE_DIR, "data", "bares.json")

with open(caminho_arquivo, "r", encoding="utf-8") as f:
    data = json.load(f)

# puxando os bares do arquivo pra memória
bares = data["features"]


# Formula de Haversine para determinar a distância entre 2 pontos em uma esfera:
# distância = 2 * R * arcsin(sqrt(sin²((lat2 - lat1)/2) + cos(lat1) * cos(lat2) * sin²((lon2 - lon1)/2)))
# OBS: Apesar da fórmula ser grande não foi tão difícil quanto eu esperava
def calcular_distancia(lat1, lon1, lat2, lon2):
    r = 6371 # raio da Terra

    # distância entre as latitudes e longitudes (convertendo pra radianos pra poder usar na fórmula)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # a fórmula separava o 'a', então botei ela aqui pra ficar mais fácil de ler, mas é só a parte dentro do sqrt da fórmula de Haversine
    a = (math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)

    # distância final
    distancia = r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return distancia

#################################################################################
# Endpoints
#################################################################################


# Botei aqui só pra testar se a API tava funcionando no começo do projeto
@app.get("/")
def home():
    return {"m":"a API ta funcionando"}

# Botei esse endpoint pra mostrar a lista dos bares carregados na memória a partir do arquivo (só pra teste mesmo, não é necessário pro funcionamento da API)
@app.get("/bares")
def listar_bares():
    return bares

# Esse que seria o endpoint chave da API, pegando os bares próximos a partir da localização do usuário, 
# usando a fórmula de Haversine pra calcular a distância entre o usuário e os bares
@app.get("/bares/proximos")
def bares_proximos(lat: float, lon: float, raio_km: float):
    resultado = []

    for bar in bares:
        coords = bar["geometry"]["coordinates"]
        lon_bar, lat_bar = coords

        distancia = calcular_distancia(lat, lon, lat_bar, lon_bar)
        # print(distancia) # mostrando a distancia no terminal pra ver se não estava invertendo as coordenadas

        if distancia <= raio_km:
            resultado.append({
                "nome": bar["properties"]["nome"],
                "endereco": bar["properties"]["endereco"],
                "latitude": lat_bar,
                "longitude": lon_bar,
                "distancia_km": distancia
            })

    return resultado