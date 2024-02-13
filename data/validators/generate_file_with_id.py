import json
import jsonschema
import sys
import requests
import uuid
import os
import generate_uris
import validators

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
    print(split_path)
    if len(split_path) > 0:
        if (len(split_path) > 3 and split_path[-4] == 'data' and split_path[-3] == 'inferlink' and split_path[-2] == 'extractions') \
                or (len(split_path) > 2 and split_path[-2] == 'umn') or (len(split_path) > 2 and split_path[-2] == 'sri'):
            is_under_data_folder = True

    return is_under_data_folder and file_extension.lower() == '.json'

filename = sys.argv[1]
new_json_folder = sys.argv[2]
file_name_without_path = os.path.basename(filename)


with open(filename) as file:
    json_data = json.load(file)

file_path = filename

print(filename, new_json_folder)

if is_json_file_under_data(file_path):
    print(f'{file_path} is a JSON file, running validation on it')

    ms_list = json_data['MineralSite']


    base_url = 'http://127.0.0.1:5007/'
    mndr_url = 'https://minmod.isi.edu/resource/'

    ms_url = base_url + 'mineral_site'
    doc_url = base_url + 'document'
    mi_url = base_url + 'mineral_inventory'

    headers = {"Content-Type": "application/json"}

    for ms in ms_list:
        if "deposit_type" in ms:
            for dp in ms['deposit_type']:
                is_valid_uri(dp)

        ms['id'] = mndr_url + mineral_site_uri(ms)

        if "location_info" in ms:
            ll = ms["location_info"]
            if "state_or_province" in ll:
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


    file_to_write = new_json_folder + '/' + file_name_without_path
    file_exists = os.path.exists(file_to_write)

    if not file_exists:
        os.makedirs(os.path.dirname(file_to_write), exist_ok=True)

    with open(file_to_write, 'w') as file:
        file.write(json.dumps(json_data, indent=2))

else:
    print(f'{file_path} is not a JSON file ..........')


