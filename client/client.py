import requests
from tkinter import messagebox

class Client:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }

    #def get_contacts():
    #    cotacts = Client().get(CONTACTS)
    #    return contacts
    def get(self, endpoint):
        response = requests.get(endpoint, headers=self.headers)
        #success_response = self._check_response(response)
        # return response.json()
        success_response = self._check_response(response)
        if success_response:
             return response.json()
        return None

    def post(self, endpoint, body):
        response = requests.post(endpoint, headers=self.headers, json=body)
        #self._check_response(response)
        # return response.json()
        success_response = self._check_response(response)
        if success_response:
            return response.json()
        return None

    def delete(self, endpoint):
        response = requests.delete(endpoint, headers=self.headers)
        # self._check_response(response)
        # return response.json()
        success_response = self._check_response(response)
        if success_response:
            return response.json()
        return None

    @staticmethod
    def _check_response(response):
        success = response.ok
        if not success:
            # raise Exception(response.content)
            messagebox.showerror("API error message", response.content)

        return success