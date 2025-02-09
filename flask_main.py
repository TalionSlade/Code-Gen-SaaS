# import google.generativeai as genai
# import requests

# import time

# def ask_ollama(prompt, model="llama2", max_retries=3):
#     """
#     Check Ollama connectivity and get response
#     """
#     base_url = "http://localhost:11434"
    
#     # Check if service is running
#     def is_ollama_running():
#         try:
#             response = requests.get(f"{base_url}/api/tags")
#             return response.status_code == 200
#         except requests.exceptions.ConnectionError:
#             return False
    
#     # Try to connect with retries
#     for attempt in range(max_retries):
#         if is_ollama_running():
#             try:
#                 response = requests.post(
#                     f"{base_url}/api/generate",
#                     json={
#                         "model": model,
#                         "prompt": prompt
#                     }
#                 )
#                 return response.json()["response"]
#             except Exception as e:
#                 return f"Error calling Ollama: {str(e)}"
#         else:
#             if attempt < max_retries - 1:
#                 print(f"Ollama not running. Retry {attempt + 1}/{max_retries}...")
#                 time.sleep(2)  # Wait 2 seconds before retrying
#             else:
#                 return "Error: Ollama service is not running. Please start with 'ollama serve'"

# def ask_gemini(prompt, api_key):
#     """
#     Simple function to get response from Gemini Pro
#     """
#     try:
#         # Configure the API
#         genai.configure(api_key=api_key)
        
#         # Initialize Gemini Pro model
#         model = genai.GenerativeModel('gemini-pro')
        
#         # Generate response
#         response = model.generate_content(prompt)
#         return response.text
    
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# def ask_ai(prompt, service="gemini", gemini_api_key=None, ollama_model="mistral"):
#     """
#     Unified function to query either Gemini Pro or Ollama
#     """
#     if service.lower() == "gemini":
#         if not gemini_api_key:
#             return "Error: Gemini API key required"
#         return ask_gemini(prompt, gemini_api_key)
    
#     elif service.lower() == "ollama":
#         return ask_ollama(prompt, model=ollama_model)
    
#     else:
#         return "Error: Invalid service specified. Use 'gemini' or 'ollama'"

# # Example usage
# api_key = "AIzaSyDv8jaIzUzP92DECo7b1ZV4Vh3SNehxCvw"
# response_gemini = ask_ai("What is Python?", service="gemini", gemini_api_key=api_key)
# # response_ollama = ask_ai("What is Python?", service="ollama", ollama_model="mistral")

import requests

def ask_codellama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "codellama",  # specifically using codellama model
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# Test it
response = ask_codellama("Write a function to calculate fibonacci numbers")
print(response)