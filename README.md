# Cirilla

<img src="https://github.com/user-attachments/assets/2e5e00d8-59b3-4d73-a967-cc04d36f85e1" style="width:100%;">
Cirilla is a Witcher-themed Telegram bot (because why not) written in Python, designed to handle a variety of IT-related tasks. I plan to incorporate some features pertaining to bug bounties in the near future. So if there are ever times you aren't at your PC, but still want to run certain tools on a target or receive push notifications about any potential changes made by a target, you can!


### Installation
Using `wget`:
```
wget https://raw.githubusercontent.com/partyh4t/Cirilla/refs/heads/main/cirilla.py
```

Using `curl`:
```
curl -O https://raw.githubusercontent.com/partyh4t/Cirilla/refs/heads/main/cirilla.py
```

Once the script is installed, you'll have to create your own bot within the Telegram, in which it'll provide you with your own bot's token. Send the bot a message, and then use that token to access `https://api.telegram.org/bot{BOT_TOKEN_HERE}/getUpdates`, which will return JSON, containing an `id` key looking something like `21xxxxx38` within the `chat` object. That'll be the `CHAT_ID` you specify in the script so the bot can send messages to the correct chat. With that done, edit the script to include both the `BOT_TOKEN` and `CHAT_ID`.

Currently the bot uses `Flask` to host a webhook, allowing Telegram to send data directly to it. Alternatively, you can utilize the `getUpdates` endpoint, which allows for polling Telegram's API to retrieve updates/messages we've sent to the bot if you don't want to open any ports or perform any port-forwarding. I'd highly recommend checking out the actual [documentation](https://core.telegram.org/bots/webhooks) as it goes way more indepth on setting up webhooks or utilizing polling.

### Usage
TODO
