import requests

class Client:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json"
        }

    def get(self, endpoint):
        response = requests.get(endpoint, headers=self.headers)
        self._check_response(response)
        return response.json()
    def post(self, endpoint, body):
        response = requests.post(endpoint, headers=self.headers)
        self._check_response(response)
        return response.json()
    def delete(self, endpoint):
        response = requests.delete(endpoint, headers=self.headers)
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response):
        if not response.ok:
            raise Exception(response.content)