from chat_app.settings import USER_NAME, PASSWORD
from client.client import Client
from client.urls import CONTACTS_ENDPOINT, AUTHENTICATE_ENDPOINT, DISCUSSIONS_ENDPOINT, MESSAGES_ENDPOINT


def get_contacts():
    contacts = Client().get(CONTACTS_ENDPOINT)
    return contacts


def authenticate():
    client = Client()
    body = {
        "name": USER_NAME,
        "password": PASSWORD
    }
    return client.post(AUTHENTICATE_ENDPOINT, body)


def get_discussions(user_id):
    client = Client()
    discussions = client.get(f"{DISCUSSIONS_ENDPOINT}/?user_id={user_id}")
    if not discussions:
        return []
    return discussions


def create_new_discussion(user_id, selected_contact_id):
    client = Client()
    body = {
        "contacts": [user_id, selected_contact_id]
    }
    return client.post(DISCUSSIONS_ENDPOINT, body)

def get_messages(user_id, discussion_id):
    messages = Client().get(f"{MESSAGES_ENDPOINT}/?user_id={user_id}&discussion_id={discussion_id}")
    if not messages:
        return []

    return messages


def create_new_message(message_obj):
    client = Client()
    return client.post(MESSAGES_ENDPOINT, message_obj)