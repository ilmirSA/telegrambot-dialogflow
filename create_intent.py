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
    with open(google_application_credentials, "r", encoding="UTF-8", ) as file:
        file_content_json = file.read()
    google_credentials = json.loads(file_content_json)
    project_id = google_credentials['project_id']

    with open('questions.json', "r", encoding="UTF-8", ) as file:
        file_content_json = file.read()
    questions = json.loads(file_content_json)
    for headline, content in questions.items():
        answers_and_questions = questions.get(headline)
        create_intent(project_id, headline, answers_and_questions['questions'], [answers_and_questions['answer']])


if __name__ == '__main__':
    main()
