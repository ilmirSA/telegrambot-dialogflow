import json
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater


def echo(update, context):
    language_code = "ru-RU"
    texts = update.message.text
    chat_id = update.effective_chat.id

    text_from_dialogue_flow = detect_intent_texts(
        project_id,
        chat_id,
        texts,
        language_code
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_from_dialogue_flow
    )


def start(update, context):
    text_message = 'Здравствуйте'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def detect_intent_texts(project_id, session_id, text, language_code):
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)

    project_id = google_application_credentials_json.get("project_id")

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
