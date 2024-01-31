from pyshacl import validate
import sys
from rdflib import Graph
import validate_pyshacl

# Temporaryily needed till all the files in main don't follow the schema

filename = sys.argv[1]
print(filename)

try:
    with open(filename, 'r') as file:
        data_graph = file.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

validate_pyshacl.validate_using_shacl(data_graph)