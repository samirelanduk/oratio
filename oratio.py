import requests

class User:
    """A user of the OpenAI API, with a token and an account.
    
    :param str token: The API token for the user.
    """

    def __init__(self, token):
        self.token = token
    

    def __repr__(self):
        truncated_token = self.token[:13] + "..." + self.token[-5:]
        return f"User({truncated_token})"
    

    def request(self, method, path, **kwargs):
        """Make an authorized request to the OpenAI API. Returns whatever JSON
        data the API responds with.
        
        :param str method: The HTTP method to use.
        :param str path: The path to request.
        :rtype: dict or list
        """

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
        """Make an authorized GET request to the OpenAI API. Returns whatever
        JSON data the API responds with.
        
        :param str path: The path to request.
        :rtype: dict or list
        """
        return self.request("GET", path)
    

    def post(self, path, **kwargs):
        """Make an authorized POST request to the OpenAI API. Returns whatever
        JSON data the API responds with.
        
        :param str path: The path to request.
        :rtype: dict or list
        """

        return self.request("POST", path, **kwargs)
    

    def models(self):
        """List the models available to the user.
        
        :rtype: list
        """

        return [m["id"] for m in self.get("models")["data"]]



class Agent:
    """An agent that can participate in conversations.
    
    :param str model: The ID of the model to use.
    :param str prompt: The initial prompt to use.
    """

    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt
    

    def __repr__(self):
        prompt = self.prompt
        if len(prompt) > 40: prompt = f"{prompt[:37]}..."
        return f"Agent({prompt})"