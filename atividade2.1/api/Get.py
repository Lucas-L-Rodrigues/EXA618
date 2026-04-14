#!/usr/bin/env python3
import os
import json
from datetime import datetime
from urllib.parse import parse_qs

qs = os.environ.get("QUERY_STRING", "")
params = parse_qs(qs, encoding="latin-1")

nome = params.get("nome", ["Anônimo"])[0]
mensagem = params.get("msg", [""])[0]
data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

postagensJSON = "postagens.json"

postagens = []


with open(postagensJSON, "r", encoding="utf-8") as f:
    try:
        postagens = json.load(f)
    except json.JSONDecodeError:
        postagens = []

if mensagem:
    nova_postagem = {
        "autor": nome,
        "data": data_hora,
        "texto": mensagem
    }

    postagens.append(nova_postagem)

    with open(postagensJSON, "w", encoding="utf-8") as f:
        json.dump(postagens, f, indent=4, ensure_ascii=False)

postagens_exibicao = list(reversed(postagens))

print("Content-type: text/html; charset=utf-8")
print()
print("<html><head><title>Blog - Lucas Lima Rodrigues</title></head>")
print("<h1>Postagens</h1>")
print("<a href='../Get.html'>Nova postagem</a><hr>")

for p in postagens_exibicao:
    print(f"<div style='border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;'>")
    print(f"<strong>{p['autor']}</strong> <small>({p['data']})</small><br>")
    print(f"<p>{p['texto']}</p>")
    print("</div>")

print("</body></html>")