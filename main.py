import tkinter as tk

from chat_app.chat_window import ChatWindow
from client.contacts import authenticate

# from client.contacts import add_new_contacts

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chat App")

    # Change font and color
    root.configure(bg="lightgray")

    response_obj = authenticate()
    user_id = str(response_obj.get("id"))

    chat_app = ChatWindow(root, user_id)
    chat_app.create_widgets()

    # Set the column and row extensions to make the window resizable."
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.geometry("800x600")
    root.mainloop()