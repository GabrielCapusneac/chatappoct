import threading
import asyncio
import tkinter as tk

from chat_app.chat_window import ChatWindow
from client.add_contact import authenticate

def start_async_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_app.chat_messages.connect_to_websocket_server())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat App")
    root.config(bg="lightgray")

    response_obj = authenticate()
    user_id = str(response_obj.get("id"))

    chat_app = ChatWindow(root, user_id)
    chat_app.create_widgets()

    # Set the column and row extensions to make the window resizable
    root.grid_columnconfigure(index=1, weight=1)
    root.grid_rowconfigure(index=0, weight=1)

    thread = threading.Thread(target=start_async_task)
    thread.start()

    root.geometry("800x600")
    root.mainloop()