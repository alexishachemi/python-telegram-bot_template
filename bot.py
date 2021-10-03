import telegram
from telegram.ext import *
import threading
import os

os.chdir(os.path.split(os.path.abspath(__file__))[0])

with open('keys.txt','r') as keys_file:
    keys = [key.split('\n')[0] for key in keys_file.readlines()]

token = keys[0]

try:
    chat_id = int(keys[1])
except:
    print('invalid chat id.')
    exit()

try:   
    updater = Updater(token=token, use_context=True)
except telegram.error.InvalidToken:
    print('Invalid token.')
    exit()

dp = updater.dispatcher

############################################
############################################

def start_command(update, context):
        update.message.reply_text('Started.')

def update(context):
    pass

############################################
############################################

def shutdown():
    updater.stop()
    updater.is_idle = False

def stop_command(update, context):
    update.message.reply_text('Stopping.')
    threading.Thread(target=shutdown).start()

def error(update, context):
    print(f'Update {update}\n###CAUSED ERROR###\n{context.error}')

def main():
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('stop',stop_command))

    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.run_repeating(callback=update, interval=60)

    print('Bot started')
    updater.start_polling()
    job_queue.start()
    updater.idle()

main()