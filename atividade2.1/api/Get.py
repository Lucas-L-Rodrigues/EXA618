from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from datetime import datetime

# Lista em memória para o teste
postagens = []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global postagens
        
        # 1. Ler o tamanho do conteúdo
        content_length = int(self.headers.get('Content-Length', 0))
        
        # 2. Ler e decodificar o corpo do JSON
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        
        # 3. Extrair os dados conforme o seu formato
        # { "action": "put", "message": "...", "author": "..." }
        action = data.get("action")
        author = data.get("author", "Anônimo")
        message = data.get("message", "")
        
        if action == "put" and message:
            nova_postagem = {
                "autor": author,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "texto": message
            }
            postagens.insert(0, nova_postagem)

        # 4. Responder ao cliente
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        response = {
            "status": "sucesso",
            "recebido": nova_postagem if message else None,
            "total_posts": len(postagens)
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        # Mantemos o GET apenas para você poder visualizar a lista pelo navegador
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(postagens).encode('utf-8'))