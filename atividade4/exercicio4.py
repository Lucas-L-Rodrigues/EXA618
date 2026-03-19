import csv
import json




locais = {"type": "FeatureCollection", "features": []}

#importar o csv
with open('estabelecimentos_sax.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #local[0] = row['tipo']
        local = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [float(row['lgt']), float(row['lat'])]}, "properties": {"nome": row['nome'], "tipo": row['tipo']}}
        locais["features"].append(local)

#escrever no json
with open('locais.json', 'w') as jsonfile:
    json.dump(locais, jsonfile)




#transformar em json
#with open('locais.json', 'w') as jsonfile:
#    json.dump(locais, jsonfile)
