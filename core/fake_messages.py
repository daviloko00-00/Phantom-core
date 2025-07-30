# social_engineering/fake_messages.py
from colorama import Fore
import time
import random

mensagens_padrao = {
    'whatsapp': [
        "Oi! Você recebeu um PIX. Clique aqui: http://bit.ly/pix-rec",
        "Você foi mencionado em um grupo: http://wa.me/...",
        "Código de verificação: 827193"
    ],
    'sms': [
        "Seu cartão foi bloqueado. Clique para desbloquear: http://bank.seguro-login.com",
        "Parabéns! Você ganhou um brinde. Retire em http://promo.bonus123.com"
    ],
    'email': [
        "Alerta de segurança: acesse sua conta imediatamente!",
        "Você tem mensagens não lidas em seu correio de voz. Veja aqui.",
        "Confirme seu login suspeito em: http://seguranca.conta.com"
    ]
}

def gerar_mensagem(tipo):
    tipo = tipo.lower()
    if tipo not in mensagens_padrao:
        print(Fore.RED + "[!] Tipo de mensagem inválido. Escolha: whatsapp, sms ou email.")
        return

    mensagem = random.choice(mensagens_padrao[tipo])
    print(Fore.CYAN + f"\n[+] Mensagem {tipo.capitalize()} Gerada:")
    print(Fore.WHITE + f"\n{mensagem}\n")
    time.sleep(1)
