from cryptography.fernet import Fernet
import base64, hashlib
import time

def ler_log():
    senha = input("Digite a senha para descriptografar o log: ")
    chave = base64.urlsafe_b64encode(hashlib.sha256(senha.encode()).digest())
    cipher = Fernet(chave)

    try:
        with open("log.enc", "rb") as f:
            print("\n=== Log Descriptografado ===")
            for linha in f:
                try:
                    texto = cipher.decrypt(linha.strip()).decode()
                    print(texto)
                except:
                    print("[!] Linha ilegível ou senha incorreta.")
    except FileNotFoundError:
        print("Arquivo de log não encontrado.")
    
    input("\nPressione Enter para voltar ao menu principal...")  # Pausa até o usuário pressionar Enter