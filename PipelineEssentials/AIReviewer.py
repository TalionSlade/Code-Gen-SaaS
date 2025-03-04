import requests
import json    
import os

def load_api_key(config_file="config.json"):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, "r") as file:
        config = json.load(file)
        return config["api_key_reviewer"]

def llmConnectorReview(prompt, model="gpt-4"):
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

def review_code(code, model="gpt-4"):
    prompt = f"""
    You are a code cleanup AI assitant. 
    Your job is to review the given code and remove presence of backticks and comments in code files 
    and add missing attributes if missing in css files.
    Here is the code:
    {code}
    Return the Original Code if no fixes else return the corrected code.
    DO NOT ADD ANY EXTRA TEXT OR COMMENTS IN THE RETURNED CODE.
    """
    reviewed_code = llmConnectorReview(prompt, model)
    return reviewed_code