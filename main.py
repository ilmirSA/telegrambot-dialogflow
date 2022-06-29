from dotenv import load_dotenv
import os
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler


def echo(update, context):
    text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def start(update, context):
    text_message = 'Здравствуйте'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_message)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
