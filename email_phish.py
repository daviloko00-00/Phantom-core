import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import random
import re
from colorama import Fore, Style
import time

class PhantomMail:
    def __init__(self):
        self.email_templates = {
            'login': 'templates/login_phish.html',
            'update': 'templates/update_alert.html',
            'security': 'templates/security_notice.html'
        }
        self.smtp_servers = {
            'gmail': 'smtp.gmail.com',
            'outlook': 'smtp.office365.com',
            'yahoo': 'smtp.mail.yahoo.com'
        }

    def verify_domain(self, email):
        """Verificação básica de formato de email"""
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def load_template(self, template_name, replacements):
        """Carrega e personaliza um template de email"""
        try:
            with open(self.email_templates[template_name], 'r') as f:
                content = f.read()
                for key, value in replacements.items():
                    content = content.replace(f'{{{key}}}', value)
                return content
        except Exception as e:
            print(Fore.RED + f"[!] Erro ao carregar template: {e}")
            return None

    def send_phish(self, sender, password, recipient, subject, template_type, replacements):
        """Envia email de phishing simulado"""
        if not self.verify_domain(sender):
            print(Fore.RED + "[!] Formato de email do remetente inválido")
            return False

        # Configura mensagem
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Carrega template
        body = self.load_template(template_type, replacements)
        if not body:
            return False

        msg.attach(MIMEText(body, 'html'))

        # Determina servidor SMTP e porta
        domain = sender.split('@')[-1]
        provider = domain.split('.')[0]

        smtp_server = self.smtp_servers.get(provider, f'smtp.{provider}.com')
        use_ssl = provider in ['gmail', 'yahoo']
        port = 465 if use_ssl else 587

        try:
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_server, port)
            else:
                server = smtplib.SMTP(smtp_server, port)
                server.starttls()

            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()

            print(Fore.GREEN + f"[+] Email enviado com sucesso para {recipient}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(Fore.RED + f"[!] Erro de autenticação: {e}")
            print(Fore.YELLOW + "→ Verifique a senha, ou use senha de aplicativo (Gmail)")
        except Exception as e:
            print(Fore.RED + f"[!] Falha ao enviar email: {e}")

        return False

    def generate_tracking_link(self, target_url):
        """Gera link de rastreamento único"""
        token = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=16))
        return f"http://track.phantomcorex.com/redirect?url={target_url}&id={token}"


def show_phishing_menu():
    """Menu de phishing integrado"""
    mail_system = PhantomMail()
    
    while True:
        print(Fore.CYAN + "\n" + " PHANTOM MAIL ".center(60, '='))
        print(Fore.WHITE + "\nSimulação de Phishing Ético\n")
        print(Fore.GREEN + "1. " + Fore.WHITE + "Enviar email de teste")
        print(Fore.GREEN + "2. " + Fore.WHITE + "Configurar templates")
        print(Fore.GREEN + "3. " + Fore.WHITE + "Verificar domínios")
        print(Fore.RED + "4. " + Fore.WHITE + "Voltar ao menu principal")
        print(Fore.CYAN + "\n" + "="*60)
        
        choice = input(Fore.YELLOW + "\nOpção: " + Fore.WHITE)
        
        if choice == '1':
            print(Fore.CYAN + "\n" + " ENVIO DE EMAIL ".center(60, '-'))
            sender = input("Seu email (remetente): ")
            password = input("Senha do email (armazenamento seguro): ")
            recipient = input("Destinatário (para testes): ")
            subject = input("Assunto do email: ")

            print("\nTemplates disponíveis:")
            for i, tpl in enumerate(mail_system.email_templates.keys(), 1):
                print(f"{i}. {tpl}")
            
            tpl_choice = input("\nEscolha o template: ")
            try:
                template_type = list(mail_system.email_templates.keys())[int(tpl_choice) - 1]
            except (ValueError, IndexError):
                print(Fore.RED + "[!] Template inválido.")
                continue

            replacements = {}
            print("\nPersonalize o template (deixe em branco para pular):")
            while True:
                key = input("Chave para substituir (ex: 'nome'): ")
                if not key:
                    break
                value = input(f"Valor para '{key}': ")
                replacements[key] = value

            mail_system.send_phish(sender, password, recipient, subject, template_type, replacements)
            input("\nPressione Enter para continuar...")

        elif choice == '2':
            print(Fore.YELLOW + "\n[!] Esta funcionalidade está em desenvolvimento")
            input("\nPressione Enter para continuar...")

        elif choice == '3':
            email = input("\nEmail para verificar (ex: teste@example.com): ")
            if mail_system.verify_domain(email):
                print(Fore.GREEN + f"\n[+] {email} tem um formato válido")
            else:
                print(Fore.RED + f"\n[!] {email} não é um email válido")
            input("\nPressione Enter para continuar...")

        elif choice == '4':
            break

        else:
            print(Fore.RED + "\n[!] Opção inválida")
            time.sleep(1)
