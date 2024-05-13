import warnings

import pandas as pd
import requests
from shapely.errors import WKTReadingError
from shapely.geometry import GeometryCollection
from shapely.wkt import dumps, loads

warnings.filterwarnings("ignore")


def safe_wkt_load(wkt_string):
    try:
        return loads(wkt_string)
    except WKTReadingError as e:
        print(f"Error converting WKT: {e}")
        return None


def sort_strings(series):
    # replace None or NaN with an empty string for sorting
    cleaned_series = series.fillna('').astype(str)
    return sorted(set(cleaned_series), key=len)


def merge_wkt(series):
    geometries = []
    for wkt in series:
        if pd.notna(wkt) and isinstance(wkt, str):
            try:
                geometry = loads(wkt)
                geometries.append(geometry)
            except Exception as e:
                print(f"Warning: Error loading WKT: {e} for WKT: {wkt}, skipping entry")

    if len(geometries) == 1:
        # return the single geometry directly
        return dumps(geometries[0])
    elif len(geometries) > 1:
        # return a GEOMETRYCOLLECTION if there are multiple geometries
        return dumps(GeometryCollection(geometries))
    else:
        # return None if there are no valid geometries
        return None


def adjust_lists(entry):
    if isinstance(entry, list):
        filtered_list = [value for value in entry if value != '']
        if len(filtered_list) == 1:
            return filtered_list[0]
        elif len(filtered_list) == 0:
            return None
    return entry


def run_sparql_query(query, endpoint='https://minmod.isi.edu/sparql', values=False):
    # add prefixes
    final_query = '''
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <https://minmod.isi.edu/resource/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX gkbi: <https://geokb.wikibase.cloud/entity/>
    PREFIX gkbt: <https://geokb.wikibase.cloud/prop/direct/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    \n''' + query
    # send query
    response = requests.post(
        url=endpoint,
        data={'query': final_query},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/sparql-results+json"  # Requesting JSON format
        },
        verify=False  # Set to False to bypass SSL verification as per the '-k' in curl
    )
    try:
        qres = response.json()
        if "results" in qres and "bindings" in qres["results"]:
            df = pd.json_normalize(qres['results']['bindings'])
            if values:
                filtered_columns = df.filter(like='.value').columns
                df = df[filtered_columns]
            return df
    except:
        return None
    
def run_minmod_query(query, values=False):
    return run_sparql_query(query, endpoint='https://minmod.isi.edu/sparql', values=values)

def run_geokb_query(query, values=False):
    return run_sparql_query(query, endpoint='https://geokb.wikibase.cloud/query/sparql', values=values)