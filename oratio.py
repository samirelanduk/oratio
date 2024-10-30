import requests

class User:

    def __init__(self, token):
        self.token = token
    

    def __repr__(self):
        truncated_token = self.token[:13] + "..." + self.token[-5:]
        return f"User({truncated_token})"
    

    def request(self, method, path, **kwargs):
        response = requests.request(
            method,
            f"https://api.openai.com/v1/{path}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            **kwargs
        )
        return response.json()
    

    def get(self, path):
        return self.request("GET", path)
    

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)


    def complete(self, messages, model="gpt-3.5-turbo"):
        return self.post(
            "chat/completions",
            json={
                "model": model,
                "messages": messages,
            }
        )