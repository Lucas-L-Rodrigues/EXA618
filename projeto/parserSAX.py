import xml.sax
import csv
import time

class Listener(xml.sax.ContentHandler):
    def __init__(self, writer):
        self.writer = writer
        self.lat = ""
        self.lon = ""
        self.tipo = ""
        self.nome = ""
        self.rua = ""
        self.numero = ""

    def startElement(self, tag, attributes):
        if tag == "node":
            self.lat = attributes.get("lat", "")
            self.lon = attributes.get("lon", "")
            self.tipo = ""
            self.nome = ""
            self.rua = ""
            self.numero = ""

        elif tag == "tag":
            k = attributes.get("k")
            v = attributes.get("v")

            if k == "name":
                self.nome = v

            elif k == "amenity":
                self.tipo = v
            # Pegando o endereço que tem em alguns (não todos)
            elif k == "addr:street":
                self.rua = v

            elif k == "addr:housenumber":
                self.numero = v

    def endElement(self, tag):
        if tag == "node":
            #Tirar os sem nome pra evitar o mesmo BO da atividade do OSM
            if self.tipo == "bar" and self.nome:
                print(f"\nNome: {self.nome}")
                print(f"lat: {self.lat}, lon: {self.lon}")

                self.writer.writerow([
                    self.lat,
                    self.lon,
                    self.nome,
                    self.rua,
                    self.numero
                ])

    def characters(self, content):
        pass


#inicio = time.perf_counter()

with open("data/bares.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["lat", "lon", "nome", "rua", "numero"])

    parser = xml.sax.make_parser()
    parser.setContentHandler(Listener(writer))

    with open("mapa/mapa.osm", "rb") as osm_file:
        parser.parse(osm_file)

#fim = time.perf_counter()

#print(f"\nTempo gasto: {fim - inicio:.2f} segundos")