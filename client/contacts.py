from chat_app.settings import CONNECTED_NAME, CONTACT_id
from client.client import Client
from client.urls import CONTACTS

def get_contacts():
    contacts = Client().get(CONTACTS)
    return contacts

def add_new_contacts():
    client = Client()
    body = {
        "name": CONNECTED_NAME,
        "id": CONTACT_id
    }
    client.post(CONTACTS, body)