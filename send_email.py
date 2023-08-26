
# from telegram import Bot

# # Replace 'YOUR_BOT_TOKEN' with your actual bot token
# bot = Bot(token='6541096647:AAGx8reEqqmEfAAjNEUOiM-x8A4YcMbMHQI')

# # Replace 'CHAT_ID' with the recipient's chat ID
# chat_id = '6541096647'

# # Send a message
# message = "Hello, this is a message from your bot!"
# bot.send_message(chat_id=chat_id, text=message)










# import asyncio
import telepot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telepot.Bot('6541096647:AAGx8reEqqmEfAAjNEUOiM-x8A4YcMbMHQI')

 
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, "Hello! Welcome to the vit AP Attendance. \n P.Suraj 21BCE7749 is absent for the class 24-08-2023  \n Ram 21BCE8523 is absent for the class 24-08-2023\n sree 21BCE9639 is absent for the class 24-08-2023\n P.sai 21BCE6359 is absent for the class 24-08-2023\n R.sham 21BCE7179 is absent for the class 24-08-2023  ")

# Start the bot's message loop
bot.message_loop(handle)

print("Listening for messages...")
while True:
    pass