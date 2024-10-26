import os
import sqlite3
import textwrap
from decimal import Decimal

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from algosdk import account, mnemonic
from algosdk.transaction import PaymentTxn
from algosdk.v2client import algod
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

ALGOD_ADDRESS = 'http://localhost:4001'
ALGOD_TOKEN = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

# ALGOD_ADDRESS = 'https://testnet-api.algonode.cloud'
# ALGOD_TOKEN = ''


class AlgorandWallet:
    def __init__(self) -> None:
        self.algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
        self.setup_database()

    def setup_database(self) -> None:
        con = sqlite3.connect('wallet.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS wallets(user_id TEXT PRIMARY KEY, address TEXT, encrypted_key TEXT)')
        con.commit()
        con.close()

    def create(self, user_id: int) -> tuple[str, str]:
        private_key, address = account.generate_account()
        seed = mnemonic.from_private_key(private_key)

        conn = sqlite3.connect('wallet.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO wallets VALUES (?, ?, ?)', [user_id, address, seed])
        conn.commit()
        conn.close()

        return address, seed

    async def send_token(self, sender: str, receiver: str, amount: int, sender_key: str) -> str:
        params = self.algod_client.suggested_params()
        unsigned_txn = PaymentTxn(
            sender, params, receiver, amount, note='Telegram wallet transfer'.encode())

        signed_txn = unsigned_txn.sign(sender_key)
        tx_id = self.algod_client.send_transaction(signed_txn)

        await self.wait_for_confirmation(tx_id)
        return tx_id

    async def wait_for_confirmation(self, tx_id: str) -> algod.AlgodResponseType:
        confirmed_txn = self.algod_client.pending_transaction_info(tx_id)
        return confirmed_txn


class TelegramBot:
    _decimals: int = 1_000_000

    def __init__(self) -> None:
        self.wallet = AlgorandWallet()

    async def start(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        msg = '''
        Welcome to the Algorand Wallet Bot!
        Available commands:
        /create - create a new wallet
        /balance - check your balance
        /send <address> <amount> - Send tokens to an address
        /game - play game'''

        await update.message.reply_text(textwrap.dedent(msg))

    async def create(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        address, seed = self.wallet.create(user_id)
        msg = f'''
        Wallet created successfully!
        Address: {address}
        Seed phrase:
        {seed}
        ⚠️ IMPORTANT: Save this seed phrase in a secure location. Never share it with anyone!
        '''

        await update.message.reply_text(textwrap.dedent(msg))

    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            args = context.args
            if len(args) != 2:
                await update.message.reply_text('Usage: /send <address> <amount>')
                return

            user_id = update.effective_user.id
            con = sqlite3.connect('wallet.db')
            cur = con.cursor()
            cur.execute('SELECT address, encrypted_key FROM wallets WHERE user_id = ?', [user_id])
            result = cur.fetchone()
            con.close()
            if not result:
                await update.message.reply_text('Please create a wallet first using /create')
                return

            receiver = args[0]
            amount = int(Decimal(args[1]) * self._decimals)  # Convert to microAlgos
            sender, seed = result
            private_key = mnemonic.to_private_key(seed)
            account_info = self.wallet.algod_client.account_info(sender)
            balance = account_info.get('amount', 0)

            assert sender != receiver, 'Sender must be different to receiver'
            assert amount >= 1, 'Amount must be greater than or equal to 1 microAlgos'
            assert balance > amount, 'Balance must be greater than amount'

            tx_id = await self.wallet.send_token(sender, receiver, amount, private_key)
            await update.message.reply_text(f'Transaction successful! Transaction ID: {tx_id}')
        except Exception as e:
            await update.message.reply_text(f'Error sending tokens: {str(e)}')

    async def balance(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        con = sqlite3.connect('wallet.db')
        cur = con.cursor()
        cur.execute('SELECT address FROM wallets WHERE user_id = ?', [user_id])
        result = cur.fetchone()
        con.close()
        if not result:
            await update.message.reply_text('Please create a wallet first using /create')
            return

        address = result[0]
        account_info = self.wallet.algod_client.account_info(address)
        balance = account_info.get('amount', 0) / self._decimals  # Convert microAlgos to Algos
        msg = f'''
        Address: {address}
        Balance: {balance} ALGO'''

        await update.message.reply_text(textwrap.dedent(msg))

    async def game(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Link game: http://127.0.0.1:8080/gold_digger.html')


if __name__ == '__main__':
    bot = TelegramBot()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', bot.start))
    app.add_handler(CommandHandler('create', bot.create))
    app.add_handler(CommandHandler('balance', bot.balance))
    app.add_handler(CommandHandler('send', bot.send))
    app.add_handler(CommandHandler('game', bot.game))

    app.run_polling()
