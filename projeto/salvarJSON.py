import csv
import json

locais = {
    "type": "FeatureCollection",
    "features": []
}

with open('data/bares.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        endereco = ", ".join(filter(None, [row['rua'], row['numero']]))

        local = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(row['lon']),
                    float(row['lat'])
                ]
            },
            "properties": {
                "nome": row['nome'],
                "endereco": endereco
            }
        }

        locais["features"].append(local)

with open('data/bares.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(locais, jsonfile, ensure_ascii=False, indent=4)

print("Até aqui funciona")