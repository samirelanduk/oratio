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


    def start_conversation_with_agent(self, agent, message):
        """Start a conversation with an agent by sending an opening message. A
        conversation is returned which can then be continued.
        
        :param Agent agent: The agent to converse with.
        :param str message: The opening message.
        :rtype: Conversation
        """

        response = Response(self.post("chat/completions", json={
            "model": agent.model,
            "messages": [
                {"role": "system", "content": agent.prompt.content},
                {"role": "user", "content": message}
            ]
        }))
        return Conversation(self, agent, [
            agent.prompt,
            Message("assistant", response.message, response)
        ])



class Agent:
    """An agent that can participate in conversations.
    
    :param str model: The ID of the model to use.
    :param str prompt: The initial prompt to use.
    """

    def __init__(self, model, prompt):
        self.model = model
        self.prompt = Message("system", prompt)
    

    def __repr__(self):
        prompt = self.prompt.content
        if len(prompt) > 40: prompt = f"{prompt[:37]}..."
        return f"Agent({prompt})"



class Response:
    """A response from an agent in a conversation. This is a wrapper around an
    OpenAI completion.
    
    :param dict json: The JSON data from the API.
    """

    def __init__(self, json):
        self.id = json["id"]
        self.created = json["created"]
        self.choices = [choice["message"]["content"] for choice in json["choices"]]
        self.prompt_tokens_used = json["usage"]["prompt_tokens"]
        self.completion_tokens_used = json["usage"]["completion_tokens"]
        self.tokens_used = json["usage"]["total_tokens"]
        self.message = self.choices[0]
    

    def __repr__(self):
        truncated = self.message
        if len(truncated) > 40: truncated = f"{truncated[:37]}..."
        return f"Response({truncated})"



class Message:
    """A message in a conversation.
    
    :param str role: The role of the message ("assistant", "system" etc.).
    :param str content: The content of the message.
    :param Response response: The API response that generated this message.
    """

    def __init__(self, role, content, response=None):
        self.role = role
        self.content = content
        self.response = response
    

    def __repr__(self):
        truncated = self.content
        if len(truncated) > 40: truncated = f"{truncated[:37]}..."
        return f"Message([{self.role}] {truncated})"



class Conversation:
    """A conversation between a user and an agent.

    :param User user: The user in the conversation.
    :param Agent agent: The agent in the conversation.
    :param list messages: The initial messages in the conversation.
    """

    def __init__(self, user, agent, messages):
        self.user = user
        self.agent = agent
        self.messages = messages
    

    def __repr__(self):
        return f"Conversation({self.agent})"