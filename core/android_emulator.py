import adbutils
import json
from datetime import datetime

import os

def conectar_dispositivo():
    client = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    return devices[0] if devices else None

def obter_info_dispositivo(device):
    modelo = device.shell("getprop ro.product.model").strip()
    versao = device.shell("getprop ro.build.version.release").strip()
    return modelo, versao

def listar_arquivos_dcim(device):
    arquivos = device.shell("ls /sdcard/DCIM/").strip().split('\n')
    return arquivos

def ler_arquivo(device, caminho):
    try:
        conteudo = device.shell(f"cat {caminho}")
        return conteudo.strip()
    except Exception as e:
        return f"[Erro ao ler {caminho}] {str(e)}"

def copiar_arquivo(device, origem, destino_local):
    os.makedirs(os.path.dirname(destino_local), exist_ok=True)
    device.pull(origem, destino_local)
    print(f"[+] Arquivo copiado de {origem} para {destino_local}")