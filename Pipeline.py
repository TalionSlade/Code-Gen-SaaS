# from .PipelineEssentials.Generator import generate_code
import requests
import json    
import os
import shutil
from langchain.tools import Tool
from jinja2 import Template
from langchain.chains import SimpleSequentialChain


def llmConnector(prompt, model="mistral"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )        
        if response.status_code == 200:
            # Ollama returns the generated text in the "response" key, not "text"
            # print(response)
            return response.json()["response"]
        else:
            raise Exception(f"Error generating code: {response.text}")            
    except requests.exceptions.JSONDecodeError as e:
        # Handle streaming responses if they occur
        responses = []
        for line in response.text.strip().split('\n'):
            try:
                data = json.loads(line)
                if 'response' in data:
                    responses.append(data['response'])
            except json.JSONDecodeError:
                continue
        return ''.join(responses) if responses else ""
        
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def create_project_structure(base_dir, structure):
    """
    Create directories and files based on a project structure.
    """
    for folder, contents in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)        
        if isinstance(contents, dict):
            create_project_structure(folder_path, contents)
        elif isinstance(contents, list):
            for file in contents:
                open(os.path.join(folder_path, file), "w").close()

def export_project(project_dir, output_format="zip"):
    """
    Export the project in the specified format.
    """
    if output_format == "zip":
        shutil.make_archive(project_dir, "zip", project_dir)
        print(f"Project exported as {project_dir}.zip")

project_structure = {
    "SampleAIApp": {
        "frontend": {
            "public": ["index.html"],
            "src": ["App.js", "index.js", "styles.css"]
        },
        "backend": {
            "app":["__init__.py"]
        },
        "requirements.txt": None,
        "Dockerfile": None,
        "README.md": None,
    }
}

def generate_app(user_stories,modelname="CodeLlama",projectname="SampleAIApp"):
    # Step 1: Generate code
    react_code = llmConnector(f"Generate only the React frontend required for: {user_stories} . Return only the raw code, no explainations ",modelname)
    cleaned_react_code = react_code.replace("```", "").strip()
    print(react_code)
    flask_code = llmConnector(f"Generate only the Flask backend required for: {user_stories} . Return only the raw code, without any comments, explanations, or markdown formatting like ``` or '''. Remove Markdown Formatting as well",modelname)
    cleaned_flask_code = flask_code.replace("```", "").strip()
    print(cleaned_flask_code)
    # Step 2: Assemble files
    create_project_structure(".", project_structure)
    with open("SampleAIApp"+"/frontend/src/App.js", "w") as f:
        f.write(cleaned_react_code)
    with open("SampleAIApp"+"/backend/app/__init__.py", "w") as f:
        f.write(cleaned_flask_code)

    # # Step 3: Compile (if needed)
    # compile_project("todo_app")

    # Step 4: Export
    export_project("SampleAIApp", output_format="zip")

# Run the pipeline
user_stories = """
As a user, I want to:
1. Add 2 number
2. Substract 2 numbers
3. Divide 2 numbers
4. Multiply 2 numbers
"""

# design_spec_frontend = llmConnector(f"With respect to the following {user_stories}, find out the design specifications for the frontend app")
# print(f" Design Spec frontend - {design_spec_frontend} \n ----------------------------------------------")
# design_spec_backend = llmConnector(f"With respect to the following {user_stories}, find out the design specifications for the backend app")
# print(f" Design Spec backend - {design_spec_backend}")
generate_app(user_stories,"CodeLlama","Calculator")