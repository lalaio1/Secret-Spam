# By: lalaio1
# Discord: lalaio1
# Date: 04/03/2024

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from colorama import init, Fore, Style
from selenium.common.exceptions import TimeoutException
import colorama
import sys


init()
def display_banner():
    colorama.init(autoreset=True)

    banner = r'''
  ██▓        ██▓ ███▄    █   ██████ ▄▄▄█████▓ ▄▄▄
 ▓██▒       ▓██▒ ██ ▀█   █ ▒██    ▒ ▓  ██▒ ▓▒▒████▄
 ▒██░       ▒██▒▓██  ▀█ ██▒░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄
 ▒██░       ░██░▓██▒  ▐██▒  ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██
 ░██████▒   ░██░▒██░   ▓██░▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒
 ░ ▒░▓  ░   ░▓  ░ ▒░   ▓ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░
 ░ ░ ▒  ░    ▒ ░░ ░░   ▒ ▒░░ ░▒  ░ ░    ░      ▒   ▒▒ ░
   ░ ░       ▒ ░   ░   ▒ ░ ░  ░  ░    ░        ░   ▒
     ░  ░    ░           ░       ░                 ░  ░
    '''

    try:
        print(Fore.RED + banner + Style.RESET_ALL)
    except UnicodeEncodeError:
        print(banner.encode('utf-8').decode(sys.stdout.encoding, 'ignore'))

display_banner()

url_end = input(f"{Fore.LIGHTMAGENTA_EX}                                                                   https://scret.me/{Style.RESET_ALL}")
full_url = f"https://scret.me/{url_end}"

message = input('Digite a mensagem: ')

num_threads = int(input('\033[32mDigite o número de BoTs: \033[37m'))
num_messages = int(input('\033[34mDigite o número de mensagens (por numero de bots): \033[37m'))
print(f'\033[33mConectando\033[37m [\033[31m{num_threads}\033[37m] \033[33mBots ...\033[37m')

lock = threading.Lock()

def send_message(message, thread_num):
    global total_messages_sent
    total_messages_sent = 0

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    
    driver = webdriver.Chrome(options=options)
    driver.get(full_url)
    
    start_time = time.time()
    
    for i in range(num_messages):
        try:
            textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-ckEbSK.cKDRhy")))
            textarea.send_keys(message)
            
            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-GhhNo.klWMez")))
            submit_button.click()
            
            confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-GhhNo.ZXtCF")))
            confirm_button.click()
            
            with lock:
                total_messages_sent += 1

            elapsed_time = time.time() - start_time
            if elapsed_time == 0:
                messages_per_minute = float('inf')  # para lidar com a divisão por zero
            else:
                messages_per_minute = total_messages_sent / (elapsed_time / 60)
        
                remaining_time = (num_messages - i - 1) / messages_per_minute
        
            print(f"""
                
                  
{Fore.RED}╔════════════════════════════════════════════════════════{Style.RESET_ALL}
{Fore.RED}║ {Fore.YELLOW}Número de BoTs: {thread_num:<35} {Fore.RED}                        {Style.RESET_ALL}
{Fore.RED}║ {Fore.GREEN}Mensagem Enviada: {i+1:<37} {Fore.RED}                              {Style.RESET_ALL}
{Fore.RED}║ {Fore.BLUE}Total de Mensagens Enviadas: {total_messages_sent:<19} {Fore.RED}    {Style.RESET_ALL}
{Fore.RED}║ {Fore.YELLOW}Mensagens por Minuto: {messages_per_minute:.2f}{' ':<18}{Fore.RED} {Style.RESET_ALL}
{Fore.RED}║ {Fore.CYAN}Tempo Restante Estimado: {remaining_time:.2f} minutos{Fore.RED}      {Style.RESET_ALL}
{Fore.RED}╚═════════════════════════════════════════════════════════════{Style.RESET_ALL}
""")

            another_message_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-fLcnxK.joWaxW")))
            another_message_button.click()
            
        except TimeoutException as e:
            new_proxy = input(f"{Fore.YELLOW}[!] Erro! Insira a próxima proxy: {Style.RESET_ALL}")
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server={new_proxy}')
            driver.quit()
            driver = webdriver.Chrome(options=options)
            driver.get(full_url)
            continue
            
        except Exception as e:
            print(f"{Fore.RED}Erro no Bot {thread_num}: {str(e)}{Style.RESET_ALL}")
            if i % 3 == 0:
                print(f"{Fore.RED}[!] Erro persistente, verifique o que está acontecendo.{Style.RESET_ALL}   Reiniciando depois de 30s")
            time.sleep(30)
            driver.get(full_url)
            continue
            
    driver.quit()

threads = []
for i in range(num_threads):
    t = threading.Thread(target=send_message, args=(message, i + 1))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
