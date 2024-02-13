import json
import jsonschema
import sys
import requests
import uuid
import os
import generate_uris
import base64
import create_ttl_files
import validators
import sys

def is_valid_uri(uri):
    return validators.url(uri)


def mineral_site_uri(data):
    response = generate_uris.mineral_site_uri(data)
    uri = response['result']
    return uri

def document_uri(data):
    response = generate_uris.document_uri(data)
    uri = response['result']
    return uri

def mineral_inventory_uri(param1):
    response = generate_uris.mineral_inventory_uri(param1)
    uri = response['result']
    return uri

def is_json_file_under_data(file_path):
    path, file_extension = os.path.splitext(file_path)
    split_path = path.split('/')
    is_under_data_folder = False
    if len(split_path) > 0:
        if (len(split_path) > 3 and split_path[-4] == 'data' and split_path[-3] == 'inferlink' and split_path[-2] == 'extractions') \
                or (len(split_path) > 2 and split_path[-2] == 'umn') or (len(split_path) > 2 and split_path[-2] == 'sri'):
            is_under_data_folder = True

    return is_under_data_folder and file_extension.lower() == '.json'

def get_filename(file_path):
    path, file_extension = os.path.splitext(file_path)
    split_path = path.split('/')
    if len(path) > 0:
        return split_path[-1]

def validate_json_schema(filename):

    with open(filename, 'r') as file:
        data_graph = file.read()

    schema = {
        "type": "object",
        "properties" : {
            "MineralSite": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties" : {
                        "id" :  {"type": ["string", "number"]},
                        "name" : {"type" : "string"},
                        "source_id" : {"type" : "string"},
                        "record_id" : {"type": ["string", "number"]},
                        "location_info": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string"},
                                "country": {"type": "string"},
                                "state_or_province": {"type": "string"},
                                "location_source_record_id": {"type": "string"},
                                "crs": {"type": "string"},
                                "location_source": {"type": "string"}
                            }
                        },
                        "deposit_type_candidate" : {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "observed_name": {"type": "string"},
                                    "source": {"type": "string"},
                                    "normalized_uri": {"type": "string"},
                                    "confidence": {"type": "string"},
                                }
                            }
                        },
                        "geology_info": {
                            "type": "object",
                            "properties": {
                                "age": {"type": "string"},
                                "unit_name": {"type": "string"},
                                "description": {"type": "string"},
                                "lithology": {"type": "string"},
                                "process": {"type": "string"},
                                "comments": {"type": "string"},
                                "environment": {"type": "string"}
                            }
                        },
                        "MineralInventory": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": ["string", "number"]},
                                    "category": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "contained_metal": {"type": "number"},
                                    "reference": {
                                        "type": "object",
                                        "properties": {
                                            "document": {
                                                "type": "object",
                                                "properties": {
                                                    "id":  {"type": ["string", "number"]},
                                                    "title": {"type": "string"},
                                                    "doi": {"type": "string"},
                                                    "uri": {"type": "string"},
                                                    "journal": {"type": "string"},
                                                    "year": {"type": "number"},
                                                    "month": {"type": "number"},
                                                    "volume": {"type": "number"},
                                                    "issue": {"type": "number"},
                                                    "description": {"type": "string"},
                                                    "authors": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    }
                                                }
                                            },
                                            "page_info": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "page": {"type": "number"},
                                                        "bounding_box": {
                                                            "type": "object",
                                                            "properties": {
                                                                "x_min": {"type": ["string", "number"]},
                                                                "x_max": {"type": ["string", "number"]},
                                                                "y_min": {"type": ["string", "number"]},
                                                                "y_max": {"type": ["string", "number"]}
                                                            },
                                                            "required": ["x_min", "x_max", "y_min", "y_max"]
                                                        }
                                                    },
                                                    "required": ["page"]
                                                }

                                            }
                                        }
                                    },
                                    "date": {"type": "string", "format": "date"},
                                    "commodity": {"type": "string"},
                                    "ore": {
                                        "type": "object",
                                        "properties": {
                                            "ore_unit": {"type": "string"},
                                            "ore_value": {"type": "number"}
                                        }
                                    },
                                    "grade": {
                                        "type": "object",
                                        "properties": {
                                            "grade_unit": {"type": "string"},
                                            "grade_value": {"type": "number"}
                                        }

                                    },
                                    "cutoff_grade": {
                                        "type": "object",
                                        "properties": {
                                            "grade_unit": {"type": "string"},
                                            "grade_value": {"type": "number"}
                                        }
                                    }
                                },
                                "required": ["reference"]
                            }
                        }
                    }
                    ,
                    "required": ["source_id", "record_id"]
                }
            }
        }
    }

    with open(filename) as file:
        json_data = json.load(file)
    json_string = json.dumps(json_data)
    mineral_site_json = json.loads(json_string)

    try:
        jsonschema.validate(instance=mineral_site_json, schema=schema)
        print("Validation succeeded")
    except jsonschema.ValidationError as e:
        print(f"Validation failed: {e}")
        raise  # Raise an exception to indicate failure

    return json_data


changed_files = sys.argv[1]
temp_file = sys.argv[2]

file_path = changed_files
if is_json_file_under_data(file_path):
    print(f'{file_path} is a JSON file, running validation on it')
    json_data = {}
    try:
        json_data = validate_json_schema(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' was deleted, skipping.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    ms_list = json_data['MineralSite']
    mndr_url = 'https://minmod.isi.edu/resource/'

    for ms in ms_list:
        if "deposit_type" in ms:
            for dp in ms['deposit_type']:
                is_valid_uri(dp)

        ms['id'] = mndr_url + mineral_site_uri(ms)
        if "location_info" in ms:
            ll = ms["location_info"]
            if "state_or_province" in ll and ll["state_or_province"] is None:
                ll["state_or_province"] = ""

        if "MineralInventory" in ms:
            mi_list = ms['MineralInventory']
            counter = 0

            for mi in mi_list:
                if "category" in mi:
                    for dp in mi['category']:
                        is_valid_uri(dp)

                if "commodity" in mi:
                    is_valid_uri(mi['commodity'])

                if "ore" in mi:
                    if "ore_unit" in mi['ore']:
                        ore = mi['ore']
                        is_valid_uri(ore['ore_unit'])

                if "grade" in mi:
                    if "grade_unit" in mi['grade']:
                        grade = mi['grade']
                        is_valid_uri(grade['grade_unit'])

                if "cutoff_grade" in mi:
                    if "grade_unit" in mi['cutoff_grade']:
                        cutoff_grade = mi['cutoff_grade']
                        is_valid_uri(cutoff_grade['grade_unit'])

                mi_data = {
                    "site": ms,
                    "id": counter
                }
                mi['id'] = mndr_url + mineral_inventory_uri(mi_data)
                counter += 1

                if "reference" in mi:
                    reference = mi['reference']
                    if "document" in reference:
                        document = reference['document']
                        doc_data = {
                            "document": document
                        }
                        document['id'] = mndr_url + document_uri(doc_data)


    filename = get_filename(file_path)
    with open(file_path, 'w') as file:
        # Write the new data to the file
        file.write(json.dumps(json_data, indent=2) + '\n')
    create_ttl_files.create_drepr_from_workflow1(file_path, filename)
else:
    print(f'{file_path} is not a JSON file')

