import requests
import json    
import os
import shutil
import re
from PipelineEssentials.AIGenerator import llmConnector
from PipelineEssentials.AIReviewer import review_code

def create_project_structure(base_dir, structure):
    for key, value in structure.items():
        folder_path = os.path.join(base_dir, key)
        if isinstance(value, dict):  # Handle nested dictionaries (subdirectories)
            os.makedirs(folder_path, exist_ok=True)
            create_project_structure(folder_path, value)
        elif isinstance(value, list):  # Handle file list
            os.makedirs(folder_path, exist_ok=True)
            for file_path in value:
                full_path = os.path.join(folder_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure all parent directories exist
                open(full_path, "w").close()
        elif isinstance(value, str):  # Handle individual files
            full_path = os.path.join(base_dir, value)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure all parent directories exist
            open(full_path, "w").close()

def export_project(project_dir, output_format="zip"):
    if output_format == "zip":
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"The directory {project_dir} does not exist.")
        shutil.make_archive(project_dir, "zip", project_dir)
        print(f"Project exported as {project_dir}.zip")

def infer_project_structure(user_story, tech_stack, file_stack, modelname="gpt-4"):
    prompt = f"""
    You are a code generator AI assistant. Your only job is to generate the project structure for 
    a new project based on the given user story and tech stack.

    Based on the following BDD and tech stack, determine the required project structure as a JSON object.
    BDD : {user_story}
    Tech Stack: {tech_stack}
    Return only a valid JSON object without any comments or extra text.
    Return the structure as a JSON object of file structure only.

    Example format:
    {{       
        "src": {{
            "main": "app.py",
            "routes": [
                "calculator.py"
            ],
            "static": {{
                "css": [
                    "styles.css"
                ],
                "js": [
                    "script.js"
                ]
            }},
            "templates": [
                "index.html"
            ]
        }},
        "tests": {{
            "unit_tests": [
                "test_calculator.py"
            ]
        }}        
    }}
    """
    
    response = llmConnector(prompt, modelname)
    print(response)
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
    code = re.sub(r"//.*?$|/\*.*?\*/|#.*?$", "", code, flags=re.MULTILINE | re.DOTALL)
    code = parse_code_blocks(code)
    return code.strip()

def parse_code_blocks(code: str) -> str:
    if not re.search(r"```([\s\S]+?)```", code):
        return code

    filtered_lines = []
    in_code_block = False
    for line in code.split('\n'):
        if line.startswith('```'):
            in_code_block = not in_code_block
            if not in_code_block:
                filtered_lines.append('\n')
            continue

        if in_code_block:
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)

def generate_code_for_files(project_structure, user_story, tech_stack, base_path="SampleAIApp", modelname="gpt-3.5-turbo"):
    for folder, contents in project_structure.items():
        folder_path = os.path.join(base_path, folder)
        
        if isinstance(contents, dict):
            generate_code_for_files(contents, user_story, tech_stack, folder_path, modelname)
        elif isinstance(contents, list):
            for file in contents:
                if isinstance(file, str):
                    file_path = os.path.join(folder_path, file)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directories exist
                    print(f"Info Log : Generating {file} file...")
                    prompt = f"""
                    You are a code generator AI assistant. Your only job is to generate the code for a file with context to the project structure and the other files 
                    generated so far. You are given a user story and tech stack to work with.

                    Generate the appropriate code for the file {file} in the project.
                    Ensure the file contains necessary dependencies to be runnable.
                    Ensure React frontend connects to Flask backend if applicable.
                    The project is based on this user story:
                    {user_story}
                    The project is using the following tech stack:
                    {tech_stack}
                    Return ONLY the raw code, no explanations or comments.
                    """
                    code = llmConnector(prompt, modelname).strip()
                    cleaned_code = clean_code(code)
                    # print(f"Info Log : Reviewing {file} file...")
                    # reviewed_code = review_code(cleaned_code, modelname)
                    with open(file_path, "w") as f:
                        f.write(cleaned_code)
                else:
                    print(f"Warning: Unexpected structure for file {file}. Skipping.")