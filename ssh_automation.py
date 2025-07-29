import paramiko
import time
from colorama import Fore, Style

class SSHAutomator:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connected = False

    def connect(self, hostname, username, password=None, key_file=None):
        try:
            if key_file:
                self.ssh.connect(hostname, username=username, key_filename=key_file)
            else:
                self.ssh.connect(hostname, username=username, password=password)
            
            self.connected = True
            print(Fore.GREEN + "\n[+] Conexão SSH estabelecida com sucesso!")
            return True
        except Exception as e:
            print(Fore.RED + f"\n[!] Falha na conexão SSH: {str(e)}")
            return False

    def execute_command(self, command):
        if not self.connected:
            print(Fore.RED + "\n[!] Não conectado a nenhum host SSH")
            return None

        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if errors:
                print(Fore.RED + f"\n[!] Erros:\n{errors}")
            
            return output
        except Exception as e:
            print(Fore.RED + f"\n[!] Erro ao executar comando: {str(e)}")
            return None

    def interactive_shell(self):
        if not self.connected:
            print(Fore.RED + "\n[!] Não conectado a nenhum host SSH")
            return

        print(Fore.YELLOW + "\n[*] Iniciando sessão interativa (digite 'exit' para sair)")
        shell = self.ssh.invoke_shell()
        
        while True:
            command = input(Fore.BLUE + "ssh> " + Style.RESET_ALL)
            if command.lower() == 'exit':
                break
            
            shell.send(command + "\n")
            time.sleep(1)
            
            while shell.recv_ready():
                print(shell.recv(1024).decode(), end='')

    def disconnect(self):
        if self.connected:
            self.ssh.close()
            self.connected = False
            print(Fore.GREEN + "\n[+] Conexão SSH encerrada com sucesso!")

def ssh_menu():
    automator = SSHAutomator()
    
    while True:
        print(Fore.CYAN + "\n" + " MENU SSH ".center(60, '='))
        print(Fore.WHITE + "\nSelecione uma operação:\n")
        print(Fore.GREEN + "1. " + Fore.WHITE + "Conectar a um host")
        print(Fore.GREEN + "2. " + Fore.WHITE + "Executar comando único")
        print(Fore.GREEN + "3. " + Fore.WHITE + "Sessão interativa")
        print(Fore.GREEN + "4. " + Fore.WHITE + "Desconectar")
        print(Fore.RED + "5. " + Fore.WHITE + "Voltar ao menu principal")
        print(Fore.CYAN + "\n" + "="*60)
        
        choice = input(Fore.YELLOW + "\nDigite sua opção (1-5): " + Fore.WHITE)
        
        if choice == '1':
            print(Fore.CYAN + "\n" + " CONEXÃO SSH ".center(60, '-'))
            host = input("Host/IP: ")
            user = input("Usuário: ")
            auth_method = input("Autenticação (1 - Senha / 2 - Chave SSH): ")
            
            if auth_method == '1':
                password = input("Senha: ")
                automator.connect(host, user, password=password)
            elif auth_method == '2':
                key_path = input("Caminho para chave SSH: ")
                automator.connect(host, user, key_file=key_path)
            else:
                print(Fore.RED + "\n[!] Opção inválida")
            
        elif choice == '2':
            if automator.connected:
                cmd = input("\nComando a executar: ")
                output = automator.execute_command(cmd)
                if output:
                    print(Fore.GREEN + "\nSaída:\n" + Fore.WHITE + output)
            else:
                print(Fore.RED + "\n[!] Conecte-se a um host primeiro")
            
        elif choice == '3':
            automator.interactive_shell()
            
        elif choice == '4':
            automator.disconnect()
            
        elif choice == '5':
            automator.disconnect()
            break
            
        else:
            print(Fore.RED + "\n[!] Opção inválida")
        
        input(Fore.YELLOW + "\nPressione Enter para continuar...")