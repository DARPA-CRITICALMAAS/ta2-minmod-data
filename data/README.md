# MinMod Knowledge Graph - Data Format

In order to deploy data to the knowledge graph in minmod, the ttl file needs to be in a specific format that follows our data schema design. In order to generate this ttl file, we would be requiring our stakeholders to submit data in a specific json format, that follow a certain structure, data types, domain and ranges for the values.
This documentation is to highlight the requirements for any data json being sent

The json files should be uploaded to the following folders:

1. [UMN](umn)
2. [SRI](sri)
3. [Inferlink](inferlink)

Commodities, deposit types, and unit names URI's need to match minmod URI's. The list of currently added entities:

1. [Commodities](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/commodities/minmod_commodities.csv)
2. [Deposit Types](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/depositTypes/minmod_deposit_types.csv)
3. [Units](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)

New entities can be added by TA2 Minmod group if required.

#### Structure of the file

The structure of the file will be similar to the example file - [example_json_file](example_mine.json)

#### Required Fields and Data types
The data types and required fields in the json are highlighted in [schema_file](datatypes.json)

#### Domain and Ranges

The domain and ranges of the json keys are highlighted as follows

- `MineralSite`
  * `source_id`: string representing source id of the mineral site
  * `record_id`: string representing record id of the mineral site
  * `name`: string representing observed name of the mineral site
  * `mineral_inventory`
    * `commodity`: URI of commodity in minmod, e.g.: _https://minmod.isi.edu/resource/Q589_. List of possible commodities and their minmod ids are defined in [commodities](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/commodities/minmod_commodities.csv)
    * `category`: enum, one of {`INFERRED`, `INDICATED`, `MEASURED`, `PROBABLE`, `PROVEN`, `ORIGINAL_RESOURCE, EXTRACTED, CUMULATIVE_EXTRACTED`}
    * `ore`
      * `ore_unit`: URI of ore unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q200_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
      * `ore_value`: value of ore in units, decimal value
    * `grade`
      * `grade_unit`: URI of grade unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q201_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
      * `grade_value`: value of grade in units, decimal value
    * `cutoff_grade`
      * `grade_unit`: URI of grade unit in minmod, e.g.: _https://minmod.isi.edu/resource/Q201_. List of possible unit names and their minmod ids are defined in [unit names](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/units/minmod_units.csv)
      * `grade_value`: value of grade in units, decimal value
    * `contained_metal`: quantity of a contained metal in an inventory item, float
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
  * `geology_info`: _TBD_
  * `deposit_type`: URI of deposit types in minmod, e.g.: _https://minmod.isi.edu/resource/Q24_. List of possible deposit types and their minmod ids are defined in [deposit types](https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data/blob/main/data/entities/depositTypes/minmod_deposit_types.csv)

## URI mapping
The automatic process of the KG (triples) generation will use the following pseudo-code to determine URI of non-blank nodes using concatenation and MD5 hashing to ensure uniqueness
 * `MineralInventory` URI = f(`commodity` (URI), `category`, `&mineral_site` (referring URI), `*document` (referred URI))
 * `MineralSite` URI = f(`source_id`, `record_id`)
 * `Document` URI = f(`doi`, `uri`, `title`, `authors[]`, `year`, `month`)
 
 (`&`: reference/inverse relation; `*`: pointer)
 
## Reconciling data
Matching entities will be denoted using the relation `owl:sameAs`.
In case new information (i.e., `csv` with two columns denoting the similar entities) is required to be added, the statements will be added as triples: `<e1_minmod_uri> owl:sameAs <e2_minmod_uri>`, etc...
