# Telegram Based Crypto Wallet

Telegram based crypto wallet use Algorand Python SDK and Telegram Bot API.

## Setup

1. Clone this repository to your local machine.
2. Ensure [Docker](https://www.docker.com/) is installed and operational. Then, install `AlgoKit` following this [guide](https://github.com/algorandfoundation/algokit-cli#install).
3. Go to folder `ROOT_PROJECT`, then run:
```shell
algokit project bootstrap all
```

4. Start Algokit localnet:
```shell
algokit localnet start
```

5. Access [Telegram BotFather](https://t.me/BotFather) to create a new bot and obtain token `telegram-bot-token`.
6. Go to folder `ROOT_PROJECT/projects/telegram-bot` and create new `.env` file with content:
```shell
TELEGRAM_BOT_TOKEN="telegram-bot-token"
```

7. Create Python virtual environment:
```shell
python -m venv .venv
```

8. Install requirements:
```shell
source .venv/bin/activate
pip install -r requirements.txt
```

9. Go to folder `ROOT_PROJECT/projects/game`, then run:
```shell
npm i
```

### Optional

Explore Algorand networks (include localnet):
```shell
algokit explore
```

## Start

1. Go to folder `ROOT_PROJECT/projects/telegram-bot`, then run:
```shell
python __main__.py
```

Leave the terminal open

2. Go to folder `ROOT_PROJECT/projects/game`, then run:
```shell
npm run http
```

Also leave the terminal open, too

3. Go to Telelegram bot created from step 5 of `Setup` and send `/start`


## Key Achievements

- User can use command `/start` to get help.
- User can use command `/create` to create a new wallet.
- User can use command `/balance` to check balance.
- User can use command `/send <address> <amount>` to send tokens to an address.
- User can use command `/game` to play game.

## Future Feature

- Deploy on cloud (BizFly Cloud, Clearsky) for production.
- Expand features, make it become full fledged wallet.
- Integrate multi chain for cross chain transaction.
- Develop ecosystem: Coin offering, integrate game, payment gateway, ...