import json
import jsonschema
import sys
import requests
import uuid
import os
import base64
import subprocess

import sys
import generate_uris
import validator_utils

sys.path.append('../pyshacl')
import validate_pyshacl

def run_drepr_on_file(datasource, model_file):
    destination = 'generated_files/ttl_files/'
    command = f' python -m drepr -r {model_file} -d default="{datasource}"'
    print('Running ... ', command)

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output_lines = result.stdout.splitlines()[2:]  # Skip the first two lines
        output_data = '\n'.join(output_lines)
        clean_content = remove_non_printable_chars(output_data)
        return output_data
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        print("Command output (if any):", e.output)
        return ''


def run_drepr_on_mineral_site(datasource):
    model_file = 'data/generator/model.yml'
    return run_drepr_on_file(datasource, model_file)


def run_drepr_on_mineral_system(datasource):
    model_file = 'data/generator/model_mineral_system.yml'
    return run_drepr_on_file(datasource, model_file)

def remove_non_printable_chars(text):
    # Remove vertical tabs and newlines
    clean_text = text.replace('\n', '').replace('\\u000b', '')
    return clean_text


def create_drepr_file_mineral_site(file_path, filename):
    file_content = run_drepr_on_mineral_site(file_path)
    validated_drepr = validate_pyshacl.validate_using_shacl_mineral_site(file_content)

    if not validated_drepr:
        print('Pyshacl Validation failed for Mineral Site')
        raise


def create_drepr_file_mineral_system(file_path, filename):
    file_content = run_drepr_on_mineral_system(file_path)
    validated_drepr = validate_pyshacl.validate_mineral_system_using_shacl(file_content)

    if not validated_drepr:
        print('Pyshacl Validation failed for pyshacl Mineral System')
        raise


def create_drepr_from_mineral_site(file_path, filename):
    generated_json_path = f'generated_files/json_files/{filename}.json'

    with open(file_path, 'r') as file:
        file_contents = file.read()
    create_drepr_file_mineral_site(file_path, filename)


def create_drepr_from_mineral_system(file_path, filename):
    generated_json_path = f'generated_files/json_files/{filename}.json'

    with open(file_path, 'r') as file:
        file_contents = file.read()
    create_drepr_file_mineral_system(file_path, filename)