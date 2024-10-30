import requests

def complete(token, messages, model="gpt-3.5-turbo"):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
        }
    )
    return response.json()