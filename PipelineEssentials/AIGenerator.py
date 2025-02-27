import requests
import json    
import os
import shutil
import re

def load_api_key(config_file="config.json"):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r") as file:
        config = json.load(file)
        return config["api_key"]

def llmConnector(prompt, model="gpt-4"):
    api_key = load_api_key()
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "n": 1,
                "stop": None,
                "temperature": 0.7
            }
        )        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            raise Exception(f"Error generating code: {response.text}")            
    except Exception as e:
        raise Exception(f"Error: {str(e)}")