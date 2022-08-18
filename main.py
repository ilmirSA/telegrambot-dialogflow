import json
import os
from pprint import pprint
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from google.cloud import dialogflow


def echo(update, context):
    language_code = "ru-RU"
    chat_id = update.message.chat_id
    text_message = update.message.text



    text_from_dialogue_flow = detect_intent_texts(
        project_id,
        chat_id,
        text_message,
        language_code
    )


    context.bot.send_message(chat_id=chat_id,text=text_from_dialogue_flow,)

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



if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    with open('questions.json', "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    questions = json.loads(file_content)
    q=[]
    m=[]
    project_id = google_application_credentials_json.get("project_id")
    for question in questions:
        q.extend(questions[question]["questions"])
        m.append(questions[question]["answer"])

    create_intent(project_id,"Как устроиться к вам на работу",q,m)





    #create_intent(project_id,'Как устроиться к вам на работу',questions,'Мой первый истанс')
    # updater = Updater(token=tg_token, use_context=True)
    # dispatcher = updater.dispatcher
    # start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)
    # echo_handler = MessageHandler(Filters.text, echo)
    #
    #
    # dispatcher.add_handler(echo_handler)
    # updater.start_polling()
