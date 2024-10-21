# Telegram Based Crypto Wallet

Telegram based crypto wallet use Python and Telegram Bot API.

## Setup

1. Clone this repository to your local machine.
2. Ensure [Docker](https://www.docker.com/) is installed and operational. Then, install `AlgoKit` following this [guide](https://github.com/algorandfoundation/algokit-cli#install).
3. Start Algokit localnet:
```shell
algokit localnet start
```

4. Access [Telegram BotFather](https://t.me/BotFather) to create a new bot and obtain token `telegram-bot-token`.
5. Go to folder `ROOT_PROJECT/projects/telegram-bot` and create new .env file with content:
```shell
TELEGRAM_BOT_TOKEN="telegram-bot-token"
```

6. Create Python virtual environments:
```shell
python -m venv .venv
```

7. Install requirements:
```shell
source .venv/bin/activate
pip install -r requirements.txt
```

8. Run:
```shell
python __main__.py
```

9. Go to Telelegram bot created from step 4 and send `/start`

## Optional

Explore Algorand networks (include localnet)
```shell
algokit explore
```
