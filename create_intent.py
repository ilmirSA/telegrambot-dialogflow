import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


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


def main():
    load_dotenv()
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(google_application_credentials, "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    google_application_credentials_json = json.loads(file_content)
    project_id = google_application_credentials_json['project_id']

    with open('questions.json', "r", encoding="UTF-8", ) as my_file:
        file_content = my_file.read()
    questions = json.loads(file_content)
    for question in questions:
        questions_job = []
        answer = []
        q = (questions[question]['questions'])
        a = (questions[question]['answer'])
        questions_job.extend(q)
        answer.append(a)
        create_intent(project_id, question, questions_job, answer)


if __name__ == '__main__':
    main()
