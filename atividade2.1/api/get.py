import json
from datetime import datetime

postagens = []

def handler(request):
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

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "sucesso",
                "autor_envio": author,
                "mensagens": postagens,
                "plataforma": "Vercel",
                "armazenamento": "Memória",
                "recebido": nova_postagem
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(postagens)
    }