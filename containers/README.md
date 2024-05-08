## Generating the TA2 outputs using Docker
Docker allows an isolated OS-level virtualization and thus a completely separate environment in which you can run the whole process without performing any additional installations on your machine.

### Building the image:
```
docker build -t container_minmod_ta2 .
```

### Running the container
To generate the file in the <hostmachine_volume>, run the following command:
```
docker run --env COMMODITY=<commodity> -v <hostmachine_volume>:/output container_minmod_ta2
```
For example:
```
docker run --env COMMODITY=nickel -v /tmp:/output container_minmod_ta2
```
Make sure that:
1. The volume you are using (on your local machine) has 'File Sharing' enabled in the Docker settings
2. You are using full paths (on both the local machine and the docker container)
3. The user running the docker command has access privlege (can be done by `sudo chmod 777 <hostmachine_volume>`)


## Outputs
The script generates several outputs, each capturing different aspects of Mineral Sites analysis based on a given input commodity (e.g., `nickel`). The expected outputs are described in the attached file `Proposed_Evaluation_for_TA2_v2.pdf`.


### A. Deposit Type Classification
This `csv` file classifies each Mineral Site (observed location) into different deposit types along with their confidence scores and other relevant metadata. File includes Mineral Site URI (`ms`), site name (`ms_name`), location information (`country`, `state_or_province`, `loc_crs`, `loc_wkt`), and the top 5 deposit classification types, environments, groups, as well as the source and confidence of each of the classifications (`top1_deposit_type`, `top1_deposit_classification_confidence`, etc).

**Filename:** `<commodity>_mineral_locations_with_deposit_types.csv`


### B. Mineral Site Locations

This `csv` file maps each Mineral Site (observed location) into different group ids to mark similar/reconciled sites (having `sameAs` relation). File includes Mineral Site URI (`ms`), site name (`ms_name`), location information (`country`, `state_or_province`, `loc_crs`, `loc_wkt`), and the assigned internal `group_id` to which the site corresponds.

**Filename:** `<commodity>_mineral_locations.csv`


### C. Grade and Tonnage Inventory
This `csv` file maps Mineral Sites to their corresponding Grade and Tonnage data. File includes columns for Mineral Site URI (`ms`), site name (`ms_name`), location information (`country`, `state_or_province`, `loc_crs`, `loc_wkt`), per-category grade and tonnage data (measured, indicated and inferred), as well as the aggregated total (`tot_contained_metal`, `total_tonnage`, `total_grade`), and the corresponding internal document id of the data (`internal_document_reference`).

**Filename:** `<commodity>_mineral_locations_with_grade_tonnage.csv`


### D. Mineral Site Data
This `csv` aggregates reconciled groups of Mineral Sites and deposits (having `sameAs` relation) in a single-row to represent a single reconciled Mineral Site instance, with top deposit type data if available (based on the max confidence within all site locations in the group).

**Filename:** `<commodity>_mineral_site_data.csv`


### E. Grade and Tonnage Models
This `csv` aggregates reconciled groups of Mineral Sites and deposits (having `sameAs` relation) in a single-row to represent a single reconciled Mineral Site instance, with selected grade and tonnage data (based on the max contained metal from all site locations in the group).

**Filename:** `<commodity>_mineral_grade_tonnage_models.csv`

