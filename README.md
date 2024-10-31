# oratio

A wrapper around the Open AI API.

## Install

```bash
pip install --upgrade https://github.com/samirelanduk/oratio/tarball/master
```

## Users

To begin with, you need a ``User`` object representing yourself - specifically your OpenAI account.

```python
from oratio import User

user = User("my-openai-key")
```

You can get a list of the model IDs that OpenAI currently makes available to you:

```python
models = user.models()
print(models)
```

## Agents

An agent is some entity you can interact with.
It is defined by a model ID and a system prompt, which tells it what persona it must adopt.

```python
from oratio import Agent

agent = Agent("gpt-3.5-turbo", "You are a very sleepy cat.")
```


## Conversations

You begin a ``Conversation`` by sending an opening message to it:

```python

conversation = user.start_conversation_with_agent(agent, "Hi, how are you?")
```

A conversation has a list of ``Message`` objects, which have a string content, and a 'role' indicating whether they are from the user or the agent.

If a ``Message`` is from the agent, it will have an associated ``Response`` object, which represents the information the API sent back for this message.
This contains alternative messages, and token usage to generate it.

You continue a conversation by sending another message:

```python

message = conversation.message("Tell me some facts about yourself.")
```

## Display

By default, the `start_conversation_with_agent` and `message` methods will print the message they produce, as well as storing it in state.
You can disable this though:

```python
conversation = user.start_conversation_with_agent(agent, "Hi, how are you?", print=False)
message = conversation.message("Tell me some facts about yourself.", print=False)
```

You can print the entire conversation history with:

```python
conversation.print()
```


## Interactivity

If you want to enter a more ChatGPT-like interaction, where you just type messages and it types back, you can call the `loop` method to enter an interactive prompt:

```python
user.start_conversation_with_agent(agent, "Hi, how are you?", loop=True)

# or...

conversation = user.start_conversation_with_agent(agent, "Hi, how are you?")
conversation.loop()
```