import json
import logging
import os
from functools import partial

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from dialogflow_api_intent import detect_intent_texts
from telegramlogshandler import TelegramLogsHandler

logger = logging.getLogger('Logger')


def answers_to_questions(project_id, update, context):
    language_code = "ru-RU"
    chat_id = update.message.chat_id
    text_message = update.message.text
    try:
        is_fallback,fulfillment_text = detect_intent_texts(
            project_id,
            chat_id,
            text_message,
            language_code

        )

        context.bot.send_message(chat_id=chat_id, text=fulfillment_text, )
    except:
        logger.exception("TG Бот упал")


def start(update, context):
    text_message = 'Здравствуйте'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def main():

    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']


    google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    with open(google_application_credentials, "r", encoding="UTF-8", ) as file:
        file_content_json = file.read()
    google_credentials = json.loads(file_content_json)
    project_id = google_credentials['project_id']

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    answers_to_questions_partial = MessageHandler(Filters.text, (partial(answers_to_questions, project_id)))

    dispatcher.add_handler(answers_to_questions_partial)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(updater, tg_chat_id))
    updater.start_polling()


if __name__ == '__main__':
    main()
