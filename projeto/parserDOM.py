from xml.dom.minidom import parse
import time


inicio = time.perf_counter()

#mínimo de 100 estabelecimentos
#exportar como CSV na mesma formatação pedida no classroom

xmlExportado = parse('f6.osm')

contagem = 0
nomes = 0
bares_ids = []
bares_nomes = []

for elemento in xmlExportado.getElementsByTagName("node"):
    contagem += 1
    for tag in elemento.getElementsByTagName("tag"):
         if tag.getAttribute("k") == "name":
             elemento.setAttribute("name", tag.getAttribute("v"))

         if tag.getAttribute("k") == "amenity" and tag.getAttribute("v") == "bar":
            bares_ids.append(elemento.getAttribute("id"))

    if elemento.getAttribute("name"):
        nomes += 1

for bar in bares_ids:
    for elemento in xmlExportado.getElementsByTagName("node"):
        if elemento.getAttribute("id") == bar:
            for tag in elemento.getElementsByTagName("tag"):
                if tag.getAttribute("k") == "name":
                    bares_nomes.append(tag.getAttribute("v"))
                    print(f"\n\nID: {bar}, Nome: {tag.getAttribute('v')}")
                    print(f"Nome: {tag.getAttribute('v')}")
                    print(f"Latitude: {elemento.getAttribute('lat')}")
                    print(f"Longitude: {elemento.getAttribute('lon')}\n")

fim = time.perf_counter()
print(f"\n\nTempo gasto: {fim - inicio:.2f} segundos")

print(f"\nTotal de elementos: {contagem}")
print(f"Total de elementos com nome: {nomes}")
print(f"Total de bares: {len(bares_ids)}")
print(f"Total de bares com nome: {len(bares_nomes)}")
print(f"Nomes dos bares: {bares_nomes}")