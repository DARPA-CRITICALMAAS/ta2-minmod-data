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
The script generates several outputs, each capturing different aspects of Mineral Sites analysis based on:
- **Commodity:** The type of commodity analyzed (e.g., nickel).
- **Output Directory:** Directory where the output files are stored. Ensure this directory exists and is writable.

### 1. Mineral Sites to Grade-Tonnage Data
This `csv` file maps Mineral Sites to their corresponding Grade and Tonnage data. File includes columns for Mineral Site URI (`ms`), site name (`ms_name`), country, state or province, location in WKT (Well-known text representation of geometry) format, total tonnage, and total grade. This output helps in understanding the quantitative measures of extracted minerals at each site.

**Filename:** `<commodity>_mineral_sites_to_grade_tonnage.csv`

### 2. Mineral Sites to Deposit Type Classification Results
This `csv` file classifies each Mineral Site into different deposit types along with their confidence scores and other relevant metadata. File includes Mineral Site URI, site name, country, state or province, location in WKT format, deposit type, confidence in deposit classification, source of deposit data, deposit group, and environmental settings.

**Filename:** `<commodity>_mineral_sites_to_deposit_types.csv`

### 3. Hyper Site (Aggregated Group of Reconciled Sites) to (extracted/observed) Mineral Sites
This `csv` links aggregated groups of sites (hyper sites with an arbitrary internal identifier) to individual Mineral Sites. File includes columns for Mineral Site URI, group ID (internal), site name, country, state or province, and location in WKT format.

**Filename:** `<commodity>_mineral_sites_hypersites.csv`