import json
import jsonschema
import sys
import requests
import uuid
import os
import generate_uris
import base64
import subprocess
import validate_pyshacl

def is_json_file(file_path):
    path, file_extension = os.path.splitext(file_path)
    print(str(path))
    split_path = path.split('/')
    is_under_data_folder = False
    if len(split_path) == 2 and split_path[0] == 'inferlink':
        is_under_data_folder = True

    return is_under_data_folder and file_extension.lower() == '.json'

def file_datasource(file_path):
    path, file_extension = os.path.splitext(file_path)
    split_path = path.split('/')
    if len(split_path) == 2 and split_path[0] == 'inferlink':
        return split_path[0]
    return ''


def run_drepr_on_file(datasource):
    destination = 'generated_files/ttl_files/'
    model_file = 'data/generator/model.yml'
    command = f' python -m drepr -r {model_file} -d default="{datasource}"'
    print('Running ... ', command)

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output_lines = result.stdout.splitlines()[2:]  # Skip the first two lines
        return '\n'.join(output_lines)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        print("Command output (if any):", e.output)
        return ''


def run_drepr_on_file_mineral_system(datasource):
    destination = 'generated_files/ttl_files/'
    model_file = 'data/generator/model_mineral_system.yml'
    command = f' python -m drepr -r {model_file} -d default="{datasource}"'
    print('Running ... ', command)

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output_lines = result.stdout.splitlines()[2:]  # Skip the first two lines
        return '\n'.join(output_lines)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        print("Command output (if any):", e.output)
        return ''
def remove_non_printable_chars(text):
    # Define a regular expression pattern to match Unicode escape sequences
    pattern = r'(\\u[0-9a-fA-F]{4})|\\u000b|\\n'
    # Replace Unicode escape sequences with an empty string
    clean_text = text.replace('\n', '').replace('\\u000b', '')

    return clean_text

def create_drepr_file(file_path, filename):
    file_content = run_drepr_on_file(file_path)
    clean_content = remove_non_printable_chars(file_content)
    validated_drepr = validate_pyshacl.validate_using_shacl(clean_content)

    if not validated_drepr:
        print('Validation failed for pyshacl')
        raise


def create_drepr_file_mineral_system(file_path, filename):
    file_content = run_drepr_on_file_mineral_system(file_path)
    clean_content = remove_non_printable_chars(file_content)

    validated_drepr = validate_pyshacl.validate_mineral_system_using_shacl(clean_content)

    if not validated_drepr:
        print('Validation failed for pyshacl')
        raise


def create_drepr_from_workflow1(file_path, filename):
    generated_json_path = f'generated_files/json_files/{filename}.json'

    with open(file_path, 'r') as file:
        file_contents = file.read()
    create_drepr_file(file_path, filename)


def create_drepr_from_mineral_system(file_path, filename):
    generated_json_path = f'generated_files/json_files/{filename}.json'

    with open(file_path, 'r') as file:
        file_contents = file.read()
    create_drepr_file_mineral_system(file_path, filename)
