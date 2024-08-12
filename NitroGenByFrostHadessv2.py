import requests
import random
import string
import time
from datetime import datetime
from colorama import init, Fore, Style
import threading

# Initialize colorama
init(autoreset=True)

def generate_random_code(length=16):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_webhook_message(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    current_time = datetime.now().strftime("%H:%M")
    if response.status_code == 204:
        print(f"{current_time} sMESSAGE ENVOYÉ")
    else:
        print(f"Nous avons pas pu envoyer le message.: {response.status_code}, Response: {response.text}")

def print_gradient_text():
    colors = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA
    ]
    text = """
███╗   ██╗██╗████████╗██████╗  ██████╗      ██████╗ ███████╗███╗   ██╗
████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗    ██╔════╝ ██╔════╝████╗  ██║
██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║    ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║    ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝    ╚██████╔╝███████╗██║ ╚████║
╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝

Made by frosthadessv2
"""
    color_index = 0
    for line in text.split("\n"):
        print(colors[color_index % len(colors)] + line)
        color_index += 1

def monitor_webhook(monitoring_webhook_url, notification_webhook_url):
    print("Verification du webhook...")
    last_message_id = None
    while True:
        response = requests.get(monitoring_webhook_url)
        if response.status_code == 200:
            messages = response.json()
            if messages:
                latest_message = messages[0]
                if latest_message['id'] != last_message_id:
                    last_message_id = latest_message['id']
                    notify_message = f"Webhook used: {latest_message['content']}"
                    send_webhook_message(notification_webhook_url, notify_message)
        time.sleep(5)

if __name__ == "__main__":
    print_gradient_text()
    webhook_url = input("Entrer le liens de votre webhook: ")
    monitoring_webhook_url = "https://discord.com/api/webhooks/your_monitoring_webhook_id/your_monitoring_webhook_token"
    notification_webhook_url = "https://discord.com/api/webhooks/1259229229812285463/QKJLaBFTKXdHc1c0GbYA4lozFGaB0WiSsUVj4D1h8Gjhfnt-yTnd9NrgxdMr4H0Lpota"

    threading.Thread(target=monitor_webhook, args=(monitoring_webhook_url, notification_webhook_url), daemon=True).start()

    while True:
        random_code = generate_random_code()
        message = f"discord.gift/{random_code}"
        send_webhook_message(webhook_url, message)
        time.sleep(2)  # Wait for 2 seconds before sending the next message
