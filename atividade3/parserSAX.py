import xml.sax
import csv
import time

class Listener(xml.sax.ContentHandler):
    def __init__(self, writer):
        self.writer = writer
        self.currentData = ""
        self.lat = ""
        self.lgt = ""
        self.tipo = ""
        self.nome = ""

    def startElement(self, tag, attributes):
        self.currentData = ""

        if tag == "node":
            self.lat = attributes.get("lat", "")
            self.lgt = attributes.get("lon", "")
            self.tipo = ""
            self.nome = ""

        if tag == "tag":
            if attributes.get("k") == "name":
                self.nome = attributes.get("v", "")
            if attributes.get("k") == "amenity":
                self.tipo = attributes.get("v", "")

    def endElement(self, tag):
        if tag == "node":
            if self.tipo and self.nome:
                print(f"\n\nNome: {self.nome}")
                print(f"Latitude: {self.lat}")
                print(f"Longitude: {self.lgt}")
                print(f"Tipo: {self.tipo}")
                self.writer.writerow([self.lat, self.lgt, self.tipo, self.nome])

    def characters(self, content):
        self.currentData += content


inicio = time.perf_counter()

with open("estabelecimentos_sax.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["lat", "lgt", "tipo", "nome"])

    parser = xml.sax.make_parser()

    Handler = Listener(writer)
    parser.setContentHandler(Handler)

    parser.parse("fsa.osm")

fim = time.perf_counter()

print(f"\nTempo gasto: {fim - inicio:.2f} segundos")