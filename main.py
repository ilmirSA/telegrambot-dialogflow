import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


# from telegram.ext import Updater
# from telegram.ext import CommandHandler
# from telegram.ext import MessageHandler, Filters, InlineQueryHandler
#
#
# def echo(update, context):
#     text = update.message.text
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text=text)
#
#
# def start(update, context):
#     text_message = 'Здравствуйте'
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text=text_message)
#
#
# def main():
#     load_dotenv()
#     tg_token = os.getenv('TG_TOKEN')
#
#     updater = Updater(token=tg_token, use_context=True)
#     dispatcher = updater.dispatcher
#     start_handler = CommandHandler('start', start)
#     dispatcher.add_handler(start_handler)
#     echo_handler = MessageHandler(Filters.text, echo)
#     dispatcher.add_handler(echo_handler)
#     updater.start_polling()
#

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)
        print(f"query_input {query_input} ")

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print(f"Query text: {response.query_result.query_text}")

        return response.query_result.fulfillment_text


def main():
    load_dotenv()
    a = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(a, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    capitals_json = json.loads(file_content)

    project_id = capitals_json.get("project_id")

    t = ["Ку", ]
    id = "123456789"
    e = "ru-RU"

    print(detect_intent_texts(project_id, id, t, e))


if __name__ == '__main__':
    main()
