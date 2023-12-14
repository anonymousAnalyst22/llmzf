import os
import requests
from pprint import pprint

def openai_completion(prompt:'str') -> 'str':
    url = "https://comp.azure-api.net/azure/openai/deployments/gpt35/completions"
    headers = {"api-key":os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"}
    body = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 512,
        "n": 1
    }
    x = requests.post(url, headers=headers, json = body)
    response_json = x.json()

def openai_chat(messages:list, temperature=1) -> tuple:
    url = "https://comp.azure-api.net/azure/openai/deployments/gpt35/chat/completions"
    headers = {"api-key":os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"}
    body = {
       "messages": messages,
       "temperature": temperature
    }
    x = requests.post(url, headers=headers, json = body)
    response_json = x.json()
    response_content = ''
    total_tokens = 0
    try:
        response_content = response_json['choices'][0]['message']['content']
        total_tokens = int(response_json['usage']['total_tokens'])
    except:
        pprint(response_json)
    return response_content, total_tokens

def query_used_tokens():
    url = 'https://comp.azure-api.net/azure/openai/used-tokens'
    headers = {"api-key":os.environ["OPENAI_API_KEY"]}
    x = requests.get(url, headers=headers)
    print(x.text)

