import json
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType


def answers_the_questions(message, vk_api):
    if message == True:
        pass
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


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
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    project_id = google_application_credentials_json['project_id']
    vk_token = os.getenv('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text_from_dialogflow = detect_intent_texts(project_id, event.user_id, event.text, 'ru-RU')
            answers_the_questions(text_from_dialogflow, vk_api)
