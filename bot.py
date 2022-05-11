from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, JobQueue
import threading

with open('token.txt','r') as f:
    TOKEN = f.read()

updater = Updater(TOKEN)
dp = updater.dispatcher

def start_command(update: Update, context: CallbackContext):
        update.message.reply_text('Started.')


def job_update(context: CallbackContext):
    pass


def shutdown():
    updater.stop()
    updater.is_idle = False


def stop_command(update: Update, context: CallbackContext):
    update.message.reply_text('Stopping.')
    threading.Thread(target=shutdown).start()


def error(update: Update, context: CallbackContext):
    print(f'Update\n{update}\ncaused error\n{context.error}')


def main():
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('stop',stop_command))

    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.run_repeating(callback=job_update, interval=60)

    print('Bot started')
    updater.start_polling()
    job_queue.start()
    updater.idle()

main()
