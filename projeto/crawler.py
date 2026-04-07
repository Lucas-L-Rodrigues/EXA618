import requests

query = """
[out:xml];
node["amenity"="bar"](-13.03, -38.54, -12.77, -38.24);
out;
"""

url = "http://overpass-api.de/api/interpreter"

response = requests.get(url, params={'data': query})

with open("mapa/mapa.osm", "wb") as f:
    f.write(response.content)


#node["amenity"="bar"](-12.32, -39.02, -12.19, -38.86); #Coordenadas de Feira de Santana
#print("Até aqui funciona")