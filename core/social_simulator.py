import datetime
from core import android_emulator

LOG_PATH = "logs/android_real_log.txt"

def registrar_log(entrada):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {entrada}\n")

def simular_eng_real():
    print("[*] Iniciando teste real de engenharia social (com consentimento)...")
    dispositivo = android_emulator.conectar_dispositivo()
    
    if not dispositivo:
        print("[!] Nenhum dispositivo ADB detectado.")
        return

    modelo, versao = android_emulator.obter_info_dispositivo(dispositivo)
    registrar_log(f"Dispositivo conectado: {modelo} (Android {versao})")

    # Listar fotos reais (nomes apenas)
    registrar_log("[*] Listando arquivos do DCIM...")
    arquivos = android_emulator.listar_arquivos_dcim(dispositivo)
    registrar_log("Arquivos encontrados:\n" + "\n".join(arquivos))

    # Tentar ler arquivo específico de interesse
    print("[?] Deseja tentar ler algum arquivo? (ex: /sdcard/Download/notes.txt)")
    caminho = input("Caminho (ou ENTER para pular): ").strip()
    if caminho:
        conteudo = android_emulator.ler_arquivo(dispositivo, caminho)
        registrar_log(f"[+] Conteúdo de {caminho}:\n{conteudo}")
        print("[✓] Conteúdo extraído e salvo no log.")

    # Copiar arquivo localmente
    print("[?] Deseja copiar algum arquivo para sua máquina?")
    origem = input("Caminho no Android (/sdcard/...): ").strip()
    destino = input("Destino local (ex: ./coletado/arquivo.txt): ").strip()
    if origem and destino:
        android_emulator.copiar_arquivo(dispositivo, origem, destino)
        registrar_log(f"[+] Arquivo copiado: {origem} → {destino}")
        print("[✓] Arquivo copiado com sucesso.")

    print("[✓] Simulação real concluída. Log salvo.")
