import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from algosdk import account
from algosdk.v2client import algod
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# algod_address = 'https://testnet-api.algonode.cloud'
# algod_token = ''

algod_address = 'http://localhost:4001'
algod_token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
algod_client = algod.AlgodClient(algod_token, algod_address)

# Dictionary to store user wallets
user_wallets = {}


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Welcome to the Algorand Wallet Bot!\nUse /create to create a new wallet or /balance to check your balance.'
    )


async def create_wallet(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_wallets:
        await update.message.reply_text('You already have a wallet!')
    else:
        private_key, address = account.generate_account()
        user_wallets[user_id] = {'private_key': private_key, 'address': address}
        await update.message.reply_text(f'Your new wallet address is: {address}')


async def check_balance(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_wallets:
        await update.message.reply_text("You don't have a wallet yet. Use /create to create one.")
    else:
        address = user_wallets[user_id]['address']
        try:
            account_info = algod_client.account_info(address)
            balance = account_info.get('amount')
            await update.message.reply_text(f'Your balance is: {balance} microAlgos')
        except Exception as e:
            await update.message.reply_text(f'Error checking balance: {str(e)}')


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('create', create_wallet))
    application.add_handler(CommandHandler('balance', check_balance))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
