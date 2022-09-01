import json
import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import Updater
from vk_api.longpoll import VkLongPoll, VkEventType


class TelegramLogsHandler(logging.Handler):

    def __init__(self, updater, tg_chat_id):
        super().__init__()
        self.tg_chat_id = tg_chat_id
        self.tg_bot = updater.bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def answers_the_questions(message, vk_api):
    try:
        if message == True:
            pass
        else:
            vk_api.messages.send(
                user_id=event.user_id,
                message=message,
                random_id=random.randint(1, 1000)
            )
    except:
        logger.exception("Бот Упал")


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return response.query_result.intent.is_fallback
    else:
        return response.query_result.fulfillment_text


if __name__ == "__main__":
    load_dotenv()
    tg_chat_id = '837743097'
    tg_token = os.getenv('TG_TOKEN')
    updater = Updater(token=tg_token, use_context=True)
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    project_id = google_application_credentials_json['project_id']
    vk_token = os.getenv('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(updater, tg_chat_id))
    updater.start_polling()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text_from_dialogflow = detect_intent_texts(project_id, event.user_id, event.text, 'ru-RU')
            answers_the_questions(text_from_dialogflow, vk_api)
