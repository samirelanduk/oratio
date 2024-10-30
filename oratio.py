import requests

class User:

    def __init__(self, token):
        self.token = token
    

    def __repr__(self):
        truncated_token = self.token[:13] + "..." + self.token[-5:]
        return f"User({truncated_token})"
    

    def complete(self, messages, model="gpt-3.5-turbo"):
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
            }
        )
        return response.json()