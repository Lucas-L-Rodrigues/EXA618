from xml.dom.minidom import parse
import csv
import time


inicio = time.perf_counter()

#mínimo de 100 estabelecimentos
#exportar como CSV na mesma formatação pedida no classroom

xmlExportado = parse('fsa.osm')

contagem = 0
nomes = 0
estabelecimentos_ids = []
estabelecimentos_nomes = []

with open('estabelecimentos.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['lat', 'lgt', 'tipo', 'nome'])
    for elemento in xmlExportado.getElementsByTagName("node"):

        contagem += 1
        for tag in elemento.getElementsByTagName("tag"):
            if tag.getAttribute("k") == "name":
                elemento.setAttribute("name", tag.getAttribute("v"))

            if tag.getAttribute("k") == "amenity":
                estabelecimentos_ids.append(elemento.getAttribute("id"))
                tipo = tag.getAttribute("v")

        if elemento.getAttribute("name"):
            nomes += 1

    for estabelecimento in estabelecimentos_ids:
        for elemento in xmlExportado.getElementsByTagName("node"):
            if elemento.getAttribute("id") == estabelecimento:
                tipo = elemento.getElementsByTagName("tag")[0].getAttribute("v")
                for tag in elemento.getElementsByTagName("tag"):
                    if tag.getAttribute("k") == "name":
                        estabelecimentos_nomes.append(tag.getAttribute("v"))
                        print(f"\n\nID: {estabelecimento}")
                        print(f"Nome: {tag.getAttribute('v')}")
                        print(f"Latitude: {elemento.getAttribute('lat')}")
                        print(f"Longitude: {elemento.getAttribute('lon')}")
                        print(f"Tipo: {tipo}")
                        lat = elemento.getAttribute("lat")
                        lgt = elemento.getAttribute("lon")
                        nome = tag.getAttribute("v")
                        writer.writerow([lat, lgt, tipo, nome])

fim = time.perf_counter()
print(f"\n\nTempo gasto: {fim - inicio:.2f} segundos")