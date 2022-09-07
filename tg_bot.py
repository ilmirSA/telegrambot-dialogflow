import json
import logging
import os


from google.cloud import dialogflow
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater


def answers_to_questions(update, context):
    try:
        language_code = "ru-RU"
        chat_id = update.message.chat_id
        text_message = update.message.text

        text_from_dialogue_flow = detect_intent_texts(
            project_id,
            chat_id,
            text_message,
            language_code
        )

        context.bot.send_message(chat_id=chat_id, text=text_from_dialogue_flow, )
    except Exception:
        logger.exception("Бот Упал")


def start(update, context):
    text_message = 'Здравствуйте'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


class TelegramLogsHandler(logging.Handler):

    def __init__(self, updater, tg_chat_id):
        super().__init__()
        self.tg_chat_id = tg_chat_id
        self.tg_bot = updater.bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


if __name__ == '__main__':

    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    project_id = google_application_credentials_json['project_id']
    print(project_id)

    # with open('questions.json', "r", encoding="UTF-8", ) as my_file:
    #     file_content = my_file.read()
    # questions = json.loads(file_content)
    # for question in questions:
    #
    #     questions_job = []
    #     answer = []
    #     q=(questions[question]['questions'])
    #     a=(questions[question]['answer'])
    #     questions_job.extend(q)
    #     answer.append(a)
    #     create_intent(project_id, question, questions_job, answer)

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    answers_to_questions_handler = MessageHandler(Filters.text, answers_to_questions)
    dispatcher.add_handler(answers_to_questions_handler)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(updater, tg_chat_id))
    updater.start_polling()
