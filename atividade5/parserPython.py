import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin


with open('seeds.txt', 'r', encoding='utf-8') as f:
    urls = [linha.strip() for linha in f.readlines() if linha.strip()]


dados = []
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=8) as response:
        html = response.read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'lxml')

    titulo = soup.title.string.strip() if soup.title else "Sem Título"
    img_tag = soup.find('img')
    img_url = img_tag.get('src') if img_tag else None
        
    dados.append({
        "titulo": titulo,
        "imagem": img_url
    })

    with open('dados.js', 'w', encoding='utf-8') as f:
        f.write("const sites = " + json.dumps(dados, indent=4, ensure_ascii=False) + ";")