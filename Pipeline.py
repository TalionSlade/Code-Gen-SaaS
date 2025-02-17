import requests
import json    
import os
import shutil
import re

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
            return response.json()["response"]
        else:
            raise Exception(f"Error generating code: {response.text}")            
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def create_project_structure(base_dir, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(contents, dict):
            create_project_structure(folder_path, contents)
        elif isinstance(contents, list):
            for file in contents:
                if isinstance(file, str):
                    open(os.path.join(folder_path, file), "w").close()
                else:
                    print(f"Warning: Unexpected structure for file {file}. Skipping.")

def export_project(project_dir, output_format="zip"):
    if output_format == "zip":
        shutil.make_archive(project_dir, "zip", project_dir)
        print(f"Project exported as {project_dir}.zip")

def infer_project_structure(user_story, tech_stack, modelname="mistral"):
    """
    Use the LLM to infer the necessary project structure dynamically based on the tech stack.
    Ensures a valid JSON response.
    """
    prompt = f"""
    Based on the following user story and tech stack, determine the required project structure (frontend and backend) as a JSON object.
    
    User story:
    {user_story}
    
    Tech stack:
    {tech_stack}
    
    Return only a valid JSON object with no explanations, comments, or extra text.
    
    Example Output:
    {{
      "frontend": {{
         "stack": "React",
         "files": ["index.html", "App.js", "styles.css"]
      }},
      "backend": {{
         "stack": "Flask",
         "files": ["app.py", "requirements.txt"]
      }}
    }}
    """
    response = llmConnector(prompt, modelname).strip()
    # print("Response -> \n",response)
    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        json_content = json_match.group(0)
    else:
        raise ValueError("Invalid JSON response from LLM")
    try:
        project_structure = json.loads(json_content)
        return project_structure
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from LLM")

def clean_code(code):
    """
    Removes comments and unnecessary text from LLM-generated code.
    """
    code = re.sub(r"//.*?$|/\*.*?\*/|#.*?$", "", code, flags=re.MULTILINE | re.DOTALL)
    return code.strip()

def ensure_imports(code, tech_stack):
    """
    Ensures essential imports are included based on the tech stack.
    """
    if "Flask" in tech_stack and "from flask" not in code:
        code = "from flask import Flask, request, jsonify\n" + code
    if "React" in tech_stack and "import React" not in code:
        code = "import React from 'react';\n" + code
    return code

def generate_code_for_files(project_structure, user_story, tech_stack, base_path="SampleAIApp", modelname="CodeLlama"):
    for folder, contents in project_structure.items():
        folder_path = os.path.join(base_path, folder)
        
        if isinstance(contents, dict):
            generate_code_for_files(contents, user_story, tech_stack, folder_path, modelname)
        elif isinstance(contents, list):
            for file in contents:
                if isinstance(file, str):
                    file_path = os.path.join(folder_path, file)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    prompt = f"""
                    Generate the appropriate code for the file {file} in the project.
                    
                    The project is based on this user story:
                    {user_story}
                    
                    The project is using the following tech stack:
                    {tech_stack}
                    
                    Return only the raw code, no explanations or comments.
                    """
                    code = llmConnector(prompt, modelname).strip()
                    cleaned_code = clean_code(code)
                    final_code = ensure_imports(cleaned_code, tech_stack)
                    with open(file_path, "w") as f:
                        f.write(final_code)
                else:
                    print(f"Warning: Unexpected structure for file {file}. Skipping.")

def generate_app(user_story, tech_stack, modelname="CodeLlama", projectname="SampleAIApp"):
    print("Inferring project structure...")
    project_structure = infer_project_structure(user_story, tech_stack, modelname)
    print("Project structure inferred:", project_structure)
    
    print("Creating project structure...")
    create_project_structure("SampleAIApp", project_structure)
    
    print("Generating code...")
    generate_code_for_files(project_structure, user_story, tech_stack, "SampleAIApp", modelname)
    
    print("Exporting project...")
    export_project("SampleAIApp", output_format="zip")
    print("Project generation complete!")

user_story = """
As a user, I want to:
1. Add 2 numbers
2. Subtract 2 numbers
3. Divide 2 numbers
4. Multiply 2 numbers
"""

tech_stack = "Frontend: React, Backend: Flask"

generate_app(user_story, tech_stack, "CodeLlama", "Calculator")
