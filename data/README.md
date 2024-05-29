# MinMod Knowledge Graph - Data Format

## Note: This page is under construction as we are aligning schemas and data at the May hackathon

In order to deploy data to the knowledge graph in minmod, the ttl file needs to be in a specific format that follows our data schema design. In order to generate this ttl file, we would be requiring our stakeholders to submit data in a specific json format, that follow a certain structure, data types, domain and ranges for the values.
This documentation is to highlight the requirements for any data json being sent

The json files should be uploaded to the following folders:

1. [UMN](umn)
2. [SRI](sri)
3. [Inferlink](inferlink/extractions)
4. [USC](usc)

Under specific folders:

1. [Mineral System](sri/mappableCriteria) The Mineral System data is added by sri

The following folders will be depreacted once code is fully migrated to a separate code repo:
1. [validators](validators)
2. [generator](generator)

Commodities, deposit types, and unit names URI's need to match minmod URI's. The list of currently added entities:

1. [Commodities](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/commodities/minmod_commodities.csv)
2. [Deposit Types](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/depositTypes/minmod_deposit_types.csv)
3. [Units](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)

New entities can be added by TA2 Minmod group if required.

[Same As](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/sameAs/sameas_mineralsites.csv) stores same as relationships between different mineral sites with different minmod URIs


#### Structure of the Mineral Site file

The structure of the file will be similar to the example file - [example_json_file](example_mine.json)

#### Structure of the Mineral System file

The structure of the file will be similar to the example file - [example_json_file](example_mineral_system.json)

#### Required Fields and Data types Mineral Site
The data types and required fields in the json are highlighted in [schema_file](datatypes.json)

#### Domain and Ranges

The domain and ranges of the json keys are highlighted as follows

- `MineralSite`
  * `source_id`: string representing source id of the mineral site
  * `record_id`: string representing record id of the mineral site
  * `name`: string representing observed name of the mineral site
  * `aliases`: list of strings representing different names of the mineral site. If there is no alias, please omit the field instead of submitting an empty list.
  * `deposit_type_candidate` (list)
    * `observed_name`: Name of deposit type candidates
    * `normalized_uri`: Minmod URI for deposit type
    * `confidence`: Confidence between 0-1 for deposit type
    * `source`: Source of deposit type candidate
  * `mineral_inventory` (list)
    * `commodity`:  (list) of commodity in minmod, e.g.: _https://minmod.isi.edu/resource/Q589_. List of possible commodities and their minmod ids are defined in [commodities](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/commodities/minmod_commodities.csv)
    * `category`: enum, one of:
      * `INFERRED` (Inferred Mineral **Resource**): Estimated based on limited geological evidence and sampling (lowest confidence level)
      * `INDICATED` (Indicated Mineral **Resource**): Estimated based on more comprehensive geological evidence and sampling (higher level of confidence)
      * `MEASURED` (Measured Mineral **Resource**): Estimated based on detailed and reliable data (highest confidence category among Mineral Resources)
      * `PROBABLE` (Probable Mineral **Reserve**): part of Indicated (and sometimes Measured) Mineral Resources that are economically mineable (lower confidence level than `PROVEN` but is considered economically viable under existing economic conditions)
      * `PROVEN` (Proven Mineral **Reserve**): highest confidence category among **Reserves** (economically mineable and is part of Measured Mineral Resources, with a high degree of confidence in the modifying factors affecting economic viability)
    * `ore`
      * `ore_unit`: (object)
        * `observed_name`: Name of unit
        * `normalized_uri`: URI of ore unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q200_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
        * `confidence`: Confidence between 0-1 for the extracted & linked unit.
        * `source`: Name of the system making the prediction
      * `ore_value`: value of ore in units, decimal value
    * `grade`
      * `grade_unit`: (object)
        * `observed_name`: Name of unit
        * `normalized_uri`: URI of grade unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q201_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
        * `confidence`: Confidence between 0-1 for the extracted & linked unit.
        * `source`: Name of the system making the prediction
      * `grade_value`: value of grade in units, decimal value
    * `cutoff_grade`
      * `grade_unit`: (object)
        * `observed_name`: Name of unit
        * `normalized_uri`: URI of grade unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q201_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
        * `confidence`: Confidence between 0-1 for the extracted & linked unit.
        * `source`: Name of the system making the prediction
      * `grade_value`: value of grade in units, decimal value
    * `contained_metal`: quantity of a contained metal in an inventory item, float
    * `zone` : Zone of a mineral inventory
    * `reference`
      * `document`
        * `title`: title of the document 
        * `doi`: doi of the document 
        * `uri`: URI of the document, if it does not have a doi
        * `authors`: list of the authors of the document, list of strings
        * `journal`: journal document belongs to
        * `year`: published year of the document, in YYYY
        * `month`: published month of the document, in m/mm
        * `volume`: volume of the document, integer
        * `issue`: issue number of the document, integer
        * `description`: description of the document
      * `page_info`: information about the page where reference of inventory is taken from (list of):
        * `page`: page number of the document
        * `bounding_box`
          * `x_min`: x axis, minimum value, decimal value
          * `x_max`: x axis, maximum value, decimal value
          * `y_min`: y axis, minimum value, decimal value
          * `y_max`: y axis, maximum value, decimal value
    * `date`: date, in the 'dd-mm-YYYY' format
    * `zone`: zone of mineral site where inventory item was discovered 
  * `location_info`
    * `location`: latitude longitude represented as `POINT (Lat Long)` in `EPSG:4326` format
    * `crs`: the coordinate reference system (CRS) in use
    * `country`: valid name of a country
    * `state_or_province`: valid state or province
  
## URI mapping
The automatic process of the KG (triples) generation will use the following pseudo-code to determine URI of non-blank nodes using concatenation and MD5 hashing to ensure uniqueness
 * `MineralInventory` URI = f(`commodity` (URI), `category`, `grade`, `ore` ,`&mineral_site` (referring URI), `*document` (referred URI))
 * `MineralSite` URI = f(`source_id`, `record_id`)
 * `Document` URI = f(`doi`, `uri`, `title`, `authors[]`, `year`, `month`)
 
 (`&`: reference/inverse relation; `*`: pointer)
 
## Reconciling data
Matching entities will be denoted using the relation `owl:sameAs`.
In case new information (i.e., `csv` with two columns denoting the similar entities) is required to be added, the statements will be added as triples: `<e1_minmod_uri> owl:sameAs <e2_minmod_uri>`, etc...
