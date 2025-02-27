import requests
import json    
import os
import shutil
import re

from PipelineEssentials.AIGenerator import llmConnector
from PipelineEssentials.ProjectManager import create_project_structure, export_project,infer_project_structure,generate_code_for_files

def generate_app(user_story, tech_stack, modelname, projectname="SampleAIApp"):
    print("Inferring project structure...")
    project_structure = infer_project_structure(user_story, tech_stack ,modelname)
    print("Project structure inferred:", project_structure)
    
    print("Creating project structure...")
    create_project_structure(projectname, project_structure)
    
    print("Generating code...")
    generate_code_for_files(project_structure, user_story, tech_stack, projectname, modelname)
    
    print("Exporting project...")
    export_project(projectname, output_format="zip")
    print("Project generation complete!")

with open(r"C:\Users\Arpan\Documents\Code-Gen-SaaS\InputBDD\calculatorBDDhtmlflask.txt", "r") as file:
    user_story = file.read()

tech_stack = "Flask"
generate_app(user_story, tech_stack, "gpt-4", "Calculator")
