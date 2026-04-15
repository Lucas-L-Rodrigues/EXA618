import json
import os
from datetime import datetime

# Caminho do arquivo JSON
DB_FILE = os.path.join(os.path.dirname(__file__), "../postagens.json")

def ler_postagens():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_postagens(postagens):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(postagens, f, ensure_ascii=False, indent=2)

def handler(request):
    postagens = ler_postagens()

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            data = {}

        action = data.get("action")
        author = data.get("author", "Anônimo")
        message = data.get("message", "")

        nova_postagem = None

        if action == "put" and message:
            nova_postagem = {
                "autor": author,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "texto": message
            }

            postagens.insert(0, nova_postagem)
            salvar_postagens(postagens)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "sucesso",
                "autor_envio": author,           # 1
                "mensagens": postagens,          # 2
                "plataforma": "Vercel",          # 3
                "armazenamento": "JSON file",    # 4
                "recebido": nova_postagem
            })
        }

    # GET → retorna todas as postagens
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(postagens)
    }