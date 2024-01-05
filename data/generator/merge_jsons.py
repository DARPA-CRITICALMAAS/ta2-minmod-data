import json
import sys
import os

folder_path = sys.argv[1]
print(folder_path)

merged_json_file = sys.argv[2]
print(merged_json_file)

list_of_jsons = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Read JSON from the file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        if 'MineralSite' in json_data:
            # Append the 'ABC' key to the merged data
            list_of_jsons.extend(json_data['MineralSite'])


        # Process the JSON data as needed
        # print(f'Processing {filename}: {json_data}')

# Read JSON from file

# print(list_of_jsons)

# Merge JSONs
merged_json = {'MineralSite': list_of_jsons}

# print(json.dumps(merged_json, indent=2))

# Write merged JSON to a new file
with open(merged_json_file, 'w') as file:
    json.dump(merged_json, file, indent=2)

print(f'Merged JSON written to merged_file.json')
