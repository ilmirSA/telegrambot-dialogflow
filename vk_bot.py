import json
import logging
import os
import random

from telegram.ext import Updater
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_api_intent import detect_intent_texts_vk
from telegramlogshandler import TelegramLogsHandler

logger = logging.getLogger('Logger')


def answers_the_questions(message, vk_bot, user_id):
    if message:
        vk_bot.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )
    else:
        pass


def main():
    while True:

        tg_chat_id = os.environ['TG_CHAT_ID']
        tg_token = os.environ['TG_TOKEN']
        google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

        with open(google_application_credentials, "r", encoding="UTF-8", ) as file:
            file_content_json = file.read()
        google_credentials = json.loads(file_content_json)
        project_id = google_credentials['project_id']

        vk_token = os.environ['VK_GROUP_TOKEN']

        vk_session = VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        long_poll = VkLongPoll(vk_session)

        updater = Updater(token=tg_token, use_context=True)
        dispatcher = updater.dispatcher
        logger.setLevel(logging.WARNING)
        logger.addHandler(TelegramLogsHandler(updater, tg_chat_id))
        try:
            for event in long_poll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text_from_dialogflow = detect_intent_texts_vk(project_id, event.user_id, event.text, 'ru-RU')
                    answers_the_questions(text_from_dialogflow, vk_api, event.user_id)
        except:
            logger.exception("VK Бот упал")


if __name__ == "__main__":
    main()
