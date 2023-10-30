import tkinter as tk
from tkinter import messagebox
import json


import asyncio
import websockets

from client.add_contact import get_messages, create_new_message
from chat_app.settings import DOMAIN, PORT


class ChatMessages(tk.Frame):
    def __init__(self, frame, discussions_list, user_id):
        super().__init__(frame)
        self.frame = frame
        self.websocket = None
        frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        self.discussions_list = discussions_list
        self.chat_text = None
        self.message_entry = None
        self.placeholder = "Type a message..."
        self.contact_id = None
        self.discussions_list.listbox_discussions.bind("<<TreeviewSelect>>", self.on_item_select)
        self.user_id = user_id

        self.create_widgets()

    async def connect_to_websocket_server(self):
        await asyncio.sleep(2)
        try:
            async with websockets.connect(f"ws://{DOMAIN}:{PORT}/ws/client_id") as websocket:
                self.websocket = websocket
                while True:
                    response = await websocket.recv()
                    if response:
                        self.on_item_select(response)
        except websockets.ConnectionClosed:
            messagebox.showerror("API error message", "Connection closed.")
        except Exception as e:
            messagebox.showerror("API error message", f"Error: {str(e)}")

    def on_item_select(self, event):
        item_id = self.discussions_list.listbox_discussions.selection()[0]
        if item_id:
            contact_data = self.discussions_list.listbox_discussions.item(item_id)
            contact_name = contact_data["text"]
            contact_id = contact_data["values"][0]
            messages = get_messages(self.user_id, contact_id)
            self.display_chat_messages(messages)

    def create_widgets(self):
        self.chat_text = tk.Text(self.frame, font=("Arial", 12))
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.message_entry = tk.Text(self.frame, font=("Arial", 12), height=2)
        self.message_entry.insert("1.0", self.placeholder)
        self.message_entry.config(fg="gray")
        # self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.bind("<FocusIn>", self.on_message_focusin)
        self.message_entry.bind("<FocusOut>", self.on_message_focusout)
        self.message_entry.pack(fill=tk.X, padx=10, pady=10)

        send_btn = tk.Button(self.frame, text="Send Message", command=self.send_message, bg="#121212", fg="white", font=("Arial", 12, "bold"))
        send_btn.pack(side=tk.RIGHT, padx=10)

    def send_message(self, event=None):
        item_id = self.discussions_list.listbox_discussions.selection()[0]
        if item_id:
            contact_data = self.discussions_list.listbox_discussions.item(item_id)
            contact_id = contact_data["values"][0]
            message = self.message_entry.get("1.0", tk.END)

            message_obj = {
                "discussion_id": contact_id,
                "user_id": self.user_id,
                "value": message
            }
            self.create_new_chat_messages(message_obj)
            asyncio.get_event_loop().run_until_complete(self.websocket.send("New Event"))
            self.message_entry.delete("1.0", tk.END)

    def create_new_chat_messages(self, message):
        create_new_message(message)

    def display_chat_messages(self, messages):
        self.chat_text.delete('1.0', tk.END)
        for message in messages:
            name = message["name"]
            value = message["value"]
            message_text = f"{name}: {value}\n"
            self.chat_text.insert(tk.END, message_text)

    def on_message_focusin(self, event):
        if self.message_entry.get("1.0", "end-1c") == self.placeholder:
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg="black")

    def on_message_focusout(self, event):
        if not self.message_entry.get("1.0", "end-1c"):
            self.message_entry.insert("1.0", self.placeholder)
            self.message_entry.config(fg="gray")

    # @staticmethod
    # def load_data(path):
    #     with open(path, "r") as f:
    #         data = json.load(f)
    #     return data