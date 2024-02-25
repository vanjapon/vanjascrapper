import telebot
import requests
import random
from datetime import datetime, timedelta
import schedule
import time

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=80)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6876479906:AAEdUWWK_Gatv2t0PG5yi4ruYNSoLci2Swg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['generate_bin'])
def generate_bin(message):
    # Get a valid BIN
    bin_number = get_valid_bin()

    # Check if the generated BIN is valid and get additional information
    bin_info = get_bin_info(bin_number)

    if bin_info:
        # Generate additional information (non-expired date)
        expiration_date = generate_non_expired_date()

        # Generate extra numbers
        extra_numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Replace 'z' with additional numbers and 'x' with original numbers
        result = f'{bin_number[:6]}{extra_numbers}xxxx|{expiration_date}'

        # Format the output
        output = f'**VANJA SCRAPPER**\n-----------------------------------------------\nBIN: {result}\nCOUNTRY: {bin_info["country"]}\nBANK: {bin_info["bank"]}\nCARD TYPE: {bin_info["card_type"].upper()}\n-----------------------------------------------\nVANJA SCRAPPER'

        # Send the result to the channel (replace 'CHANNEL_ID' with your actual channel ID)
        bot.send_message('-1001920264809', output, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Unknown BIN or Bank. Please try again.")

def get_valid_bin():
    # You might need to adjust this based on the range of valid BINs
    return ''.join([str(random.randint(4, 5))] + [str(random.randint(0, 9)) for _ in range(5)])

def get_bin_info(bin_number):
    # Make a request to binlist.net
    url = f'https://lookup.binlist.net/{bin_number}'
    response = requests.get(url)

    if response.status_code == 200:
        bin_info = response.json()
        country = bin_info.get('country', {}).get('name', 'Unknown')
        bank = bin_info.get('bank', {}).get('name', 'Unknown')
        card_type = bin_info.get('scheme', 'Unknown')

        # Only return information if the bank is known
        if bank != 'Unknown':
            return {'country': country, 'bank': bank, 'card_type': card_type}
    return None

def generate_non_expired_date():
    current_year = datetime.now().year
    expiration_year = random.randint(current_year, current_year + 3)

    # Ensure the expiration month is in the future
    if expiration_year == current_year:
        expiration_month = random.randint(datetime.now().month, 12)
    else:
        expiration_month = random.randint(1, 12)

    return f'{expiration_month:02d}|{expiration_year}'

# Schedule the task to generate a BIN every 5 seconds
schedule.every(10).seconds.do(lambda: generate_and_send_bin())

def generate_and_send_bin():
    # Get a valid BIN
    bin_number = get_valid_bin()

    # Check if the generated BIN is valid and get additional information
    bin_info = get_bin_info(bin_number)

    if bin_info:
        # Generate additional information (non-expired date)
        expiration_date = generate_non_expired_date()

        # Generate extra numbers
        extra_numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Replace 'z' with additional numbers and 'x' with original numbers
        result = f'{bin_number[:6]}{extra_numbers}xxxx|{expiration_date}'

        # Format the output
        output = f'**VANJA SCRAPPER**\n-----------------------------------------------\nBIN: {result}\nCOUNTRY: {bin_info["country"]}\nBANK: {bin_info["bank"]}\nCARD TYPE: {bin_info["card_type"].upper()}\n-----------------------------------------------\nVANJA SCRAPPER'

        # Send the result to the channel (replace 'CHANNEL_ID' with your actual channel ID)
        bot.send_message('-1001920264809', output, parse_mode='Markdown')

if __name__ == "__main__":
  keep_alive()
  while True:
        schedule.run_pending()
        time.sleep(0.1)
