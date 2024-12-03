
# Cirilla Telegram Bot

import requests, subprocess
from flask import Flask, request

BOT_TOKEN = "BOT_TOKEN_HERE"
CHAT_ID = "CHAT_ID_HERE" # Chat specific chat_id. Can be extracted from get_updates if we want to support chats with other users.

app = Flask(__name__)

# Used to get_updates (polling), rather than webhook.
'''
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset} if offset else {}
    response = requests.get(url, params=params)
    return response.json()

def main():
    print("Cirilla has awoken...")
    update_id = None
    
    while True:
        
        update = get_updates(update_id)
        for result in update.get("result", []):
            message = result.get("message", {})
            text = message.get("text")

            if text:
                print("Recevied command: " + text)
                cmd_response = handle_command(text)
                if cmd_response:
                   send_message(cmd_response)

            update_id = result["update_id"] + 1
        time.sleep(5)    
'''

# Handles the received command from get_updates.
def handle_command(cmd):
    commands = ['/commands' , '/fetch_ip', '/ssh_status']
    if cmd in commands:
        if cmd == "/commands":
            send_message(f"Commands: {commands}")
        elif cmd == "/fetch_ip":
            fetch_ip()
        elif cmd == "/ssh_status":
            ssh_status()
        else:
            return False
    else:
        send_message(f"Hello!")

# handles callbacks if a user presses an inline button
def handle_callback(cmd, id, message_id):
    if cmd == "restart_ssh":
        ssh_restart(id, message_id)
    if cmd == "Do Nothing":
        send_message(" ", inline_kb=None, callback_id=id, message_id=message_id)

# Sends the response to the user via Telegram API calls.
def send_message(cmd_response, inline_kb=None, callback_id=None, message_id=None):
    endpoint = "sendMessage"
    payload = {"chat_id": CHAT_ID, "text": cmd_response}
    if callback_id:
        endpoint = "answerCallbackQuery"
        payload["callback_query_id"] = callback_id
    if inline_kb:
        payload["reply_markup"] = {"inline_keyboard": inline_kb}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{endpoint}"
    edit_markup_url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup"
    requests.post(url, json=payload)
    if message_id:
        new_payload = {"chat_id": CHAT_ID, "message_id": message_id, "reply_markup": {"inline_keyboard": []}}
        print(new_payload)
        requests.post(edit_markup_url, json=new_payload)


# Grabs public IP address since IP is dynamic.
def fetch_ip():
    ip = requests.get('https://api.ipify.org')
    send_message(f"Current IP address is: {ip.content.decode('utf-8')}")

# Fetches current SSH server status.
def ssh_status():
    inline_keyboard = [
        [
            {"text": "Restart SSH", "callback_data": "restart_ssh"},
            {"text": "Do Nothing", "callback_data": "no_action"}
        ]
    ]
    output = subprocess.run("systemctl status ssh", shell=True, capture_output=True, text=True).stdout
    lines = output.splitlines()
    send_message(lines[2].strip(), inline_keyboard)
    
def ssh_restart(id, message_id):
    subprocess.run("systemctl restart ssh", shell=True, text=True)
    response = "SSH Restarted"
    send_message(response, inline_kb=None, callback_id=id, message_id=message_id)


# Flask Server
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    print(update)
    message = update.get("message", {})
    text = message.get("text")
    if text:
        print("Recevied command: " + text)
        handle_command(text)
    elif update.get("callback_query"):
        callback = update.get("callback_query", {})
        text = callback.get("data")
        id = callback.get("id")
        message = callback.get("message", {})
        message_id = message.get("message_id")
        if text:
            handle_callback(text, id, message_id)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=7777, host='0.0.0.0')




