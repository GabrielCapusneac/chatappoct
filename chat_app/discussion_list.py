import tkinter as tk
from tkinter import ttk
import json

from chat_app.settings import USER_NAME
from client.add_contact import get_contacts, get_discussions, create_new_discussion


class DiscussionList(tk.Frame):
    def __init__(self, frame, root, user_id):
        super().__init__(frame)
        self.frame = frame
        frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        self.root = root
        self.user_id = user_id

        self.listbox_discussions = None
        self.discussion_list = None
        self.contacts = None
        self.listbox_contacts = None

        self.create_widgets()

    def create_widgets(self):
        connected_username = tk.Label(self.frame, text=USER_NAME, bg="slategray", fg="white", font=("Arial", 12, "bold"))
        connected_username.pack(fill=tk.BOTH)

        new_chat_btn = tk.Button(self.frame, text="New Chat", command=self.open_contact_popup, font=("Arial", 12, "bold"), bg="#121212", fg="white")
        new_chat_btn.pack(fill=tk.X, pady=10)

        self.listbox_discussions = ttk.Treeview(self.frame, selectmode="browse")
        self.listbox_discussions.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox_discussions.heading("#0", text="Discussions")
        self.load_discussions()

    def open_contact_popup(self):
        # self.contacts = self.load_data("D:\\App\\resources\\contacts.json")
        self.contacts = get_contacts()

        contacts_popup = tk.Toplevel(self.root, pady=10, padx=10)
        contacts_popup.title("Contacts")

        listbox_label = tk.Label(contacts_popup, text="Contacts", bg="slategray", fg="white", font=("Arial", 12, "bold"))
        listbox_label.pack(fill=tk.BOTH, pady=10)

        self.listbox_contacts = ttk.Treeview(contacts_popup, selectmode="browse")
        self.listbox_contacts.heading("#0", text="Contacts")
        self.listbox_contacts.pack(fill=tk.BOTH, expand=True)
        self.load_contacts()

        add_contact_btn = tk.Button(contacts_popup, command=self.add_contact, text="Add Contact", font="Arial 12 bold", bg="#121212", fg="white")
        add_contact_btn.pack(fill=tk.BOTH, pady=10)

    def load_discussions(self):
        # initial_discussions = self.load_data("D:\\App\\resources\\discussions.json")
        initial_discussions = get_discussions(self.user_id)
        for discussion in initial_discussions:
            self.listbox_discussions.insert("", "end", text=discussion["name"], values=discussion["id"])

    def load_contacts(self):
        for contact in self.contacts:
            self.listbox_contacts.insert("", "end", text=contact["name"], values=contact["id"])

    def add_contact(self):
        item_id = self.listbox_contacts.selection()[0]
        if item_id:
            contact_data = self.listbox_contacts.item(item_id)
            contact_name = contact_data["text"]
            contact_id = contact_data["values"][0]

            # self.discussion_list = self.load_data("D:\\App\\resources\\discussions.json")
            new_discussion = create_new_discussion(self.user_id, contact_id)
            # self.discussion_list.append({"name": contact_name, "id": contact_id})

            # with open("D:\\App\\resources\\discussions.json", "w") as outfile:
            #     outfile.write(json.dumps(self.discussion_list, indent=4))
            self.listbox_discussions.insert("", "end", text=contact_name, values=contact_id)

    @staticmethod
    def load_data(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data