import socket
import time

def verificar_porta(host, porta):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((host, porta))
        print(f"[+] Porta {porta} ABERTA")
        s.close()
    except:
        print(f"[-] Porta {porta} FECHADA")

def scan():
    ip = input("Digite o IP do host: ")
    try:
        socket.inet_aton(ip)
    except socket.error:
        print("IP inválido.")
        time.sleep(2)  # Pausa para o usuário ler a mensagem de erro
        return

    entrada = input("Portas (separadas por vírgula): ")
    if entrada.strip():
        portas = [int(p.strip()) for p in entrada.split(',') if p.strip().isdigit()]
    else:
        portas = list(range(20, 1025))

    for porta in portas:
        verificar_porta(ip, porta)
        time.sleep(0.1)

    print("\nVarredura concluída.")
    print("As portas verificadas foram:", portas)
    input("\nPressione Enter para voltar ao menu principal...")  # Pausa até o usuário pressionar Enter