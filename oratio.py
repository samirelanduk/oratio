import time
import random
import requests

class User:
    """A user of the OpenAI API, with a token and an account.
    
    :param str openai_key: The API key for the user.
    """

    def __init__(self, openai_key):
        self.openai_key = openai_key
    

    def __repr__(self):
        truncated_key = self.openai_key[:13] + "..." + self.openai_key[-5:]
        return f"User({truncated_key})"
    

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
                "Authorization": f"Bearer {self.openai_key}",
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


    def start_conversation_with_agent(self, agent, message, print=True, typed=True, loop=False):
        """Start a conversation with an agent by sending an opening message. A
        conversation is returned which can then be continued.
        
        :param Agent agent: The agent to converse with.
        :param str message: The opening message.
        :param bool print: Whether to print the message the agent returns.
        :param bool typed: Whether to type out the message the agent returns.
        :param bool loop: Whether to start a loop that continuously prompts.
        :rtype: Conversation
        """

        response = Response(self.post("chat/completions", json={
            "model": agent.model,
            "messages": [
                {"role": "system", "content": agent.prompt.content},
                {"role": "user", "content": message}
            ]
        }))
        user_message = Message("user", message)
        message = Message("assistant", response.message, response)
        if print: message.print(typed=typed)
        conversation = Conversation(self, agent, [agent.prompt, user_message, message])
        if loop: conversation.loop(typed=typed)
        return conversation



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
    

    def to_dict(self):
        """Converts the message to a dictionary, in the format expected by the
        OpenAI API.
        
        :rtype: dict
        """

        return {"role": self.role, "content": self.content}


    def print(self, typed=False):
        """Prints the message to the console, optionally typing it out one
        character at a time.
        
        :param bool typed: Whether to type out the message.
        """

        if not typed:
            print(self.content)
            return
        for char in self.content:
            delay = random.uniform(0.01, 0.05)
            print(char, end="", flush=True)
            time.sleep(delay)
        print()



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
    

    def to_list(self):
        """Converts the conversation to a list of dictionaries, in the format
        expected by the OpenAI API.

        :rtype: list
        """

        return [message.to_dict() for message in self.messages]
    

    def message(self, content, print=True, typed=True):
        """Continue a conversation by sending a message to the agent.
        
        :param str content: The message to send.
        :param bool print: Whether to print the message the agent returns.
        :param bool typed: Whether to type out the message the agent returns.
        :rtype: Message
        """

        self.messages.append(Message("user", content))
        response = Response(self.user.post("chat/completions", json={
            "model": self.agent.model,
            "messages": [
                *self.to_list(),
                {"role": "user", "content": content}
            ]
        }))
        message = Message("assistant", response.message, response)
        if print: message.print(typed=typed)
        self.messages.append(message)
        return message


    def loop(self, typed=True):
        """Continuously prompt the user for messages and respond to them until
        the user types "exit".
        
        :param bool typed: Whether to type out the messages the agent returns.
        """

        while True:
            print()
            message = input("> ")
            print()
            if message == "exit": break
            self.message(message, typed=typed)


    def print(self):
        """Prints the conversation to the console."""

        for message in self.messages:
            print(f"[{message.role}]")
            message.print()
            print()
    

    @property
    def tokens_used(self):
        """
        The total number of tokens used in the conversation.
        
        :rtype: int
        """

        return sum(message.response.tokens_used for message in self.messages if message.response)