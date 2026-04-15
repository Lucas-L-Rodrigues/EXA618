from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

postagens = []

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        global postagens

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        data = json.loads(body.decode('utf-8'))

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

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        response = {
            "status": "sucesso",
            "autor_envio": author,                     # 1) responsável
            "mensagens": postagens,                   # 2) todas mensagens
            "plataforma": "Vercel",                  # 3) plataforma
            "armazenamento": "Memória (RAM)",        # 4) banco usado
            "recebido": nova_postagem
        }

        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        self.wfile.write(json.dumps(postagens).encode('utf-8'))