## Generating the TA2 outputs using Docker
Docker allows an isolated OS-level virtualization and thus a completely separate environment in which you can run the whole process without performing any additional installations on your machine.

### Building the image:
```
docker build -t container_ttl_generate_and_deploy .
```

### Running the container

To get help on what each parameter of the script does, run the following

```
docker run --env param1=-h container_ttl_generate_and_deploy
```
Output will be similar to this:

```
Usage: ./generateKG.sh [ARGUMENT1] [ARGUMENT2] [ARGUMENT3] ...
This script generates a ttl from input data
Arguments:
  ARGUMENT1: type of CDR - string = 'github' or 'CDR' / help (-h)
  ARGUMENT2: Location of CDR data = 'repo_location'or 'CDR_location'
  ARGUMENT3: auth token if needed
  ARGUMENT4: Master folder whose subdirectories has data - data/ for github
 docker run -e param1=github -e param2='https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data' -e param3=abc -e param4=data/ -e param5=/mindmod/generated_data  -v /tmp:/app/generated_data/ -d -p 3030:3030 container_ttl_generate_and_deploy

```
To generate all the output files in the <hostmachine_volume>, run the following command:
```
docker run -e param1=p1 -e param2=p2 -e param3=p3 ..... -v <hostmachine_volume>:/app/generated_data/ container_ttl_generate_and_deploy
```

For example:
```
docker run -e param1=github -e param2='https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data' -e param3=abc -e param4=data/  -v /tmp:/app/generated_data/ container_ttl_generate_and_deploy```
```

If you also want the script to expose the generated ttl as a sparql endpoint on port 3030 on your machine, use the following command:
(note that param5 is set to 1)
```
docker run -e param1=p1 -e param2=p2 -e param3=p3 .....param5=1 -v <hostmachine_volume>:/app/generated_data/ -p 3030:3030 container_ttl_generate_and_deploy
```

For example:
```
docker run -e param1=github -e param2='https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data' -e param3=abc -e param4=data/ -e param5=1  -v /tmp:/app/generated_data/ -d -p 3030:3030 container_ttl_generate_and_deploy```
```
Make sure that:
1. The volume you are using (on your local machine) has 'File Sharing' enabled in the Docker settings
2. You are using full paths (on both the local machine and the docker container)
3. The user running the docker command has access privlege (can be done by `sudo chmod 777 <hostmachine_volume>`)


## Outputs
The script generates ttl and json files and adds them to relvant folder. The folder location is decided by the <hostmachine_volume> given by the user. For instance in the above example, the output will be generated under /tmp. The folder structure will look like:

```
\tmp
 ---json_files
    ---umn/
    ---inferlink/
    ---sri/
       ---mappableCriteria/
  ---ttl_files
    ---umn/
    ---inferlink/
    ---usc/
    ---sri/
       ---mappableCriteria/
    ---final_kg_file.ttl
```
- final_kg_file.ttl is the final generated file
- json_files has intermediate json files, with the jsons for respective data sources in respective folders
- ttl_files has intermediate json files, with the jsons for respective data sources in respective folders
- if param5 is set to 1, final_kg_file.ttl is exposed via SPARQL endpoint on 3030. This is accessible via http://localhost:3030/minmod/sparql
  - Example query to run on this endpoint 
  ```
  curl -k -X POST http://localhost:3030/minmod/sparql --data-urlencode query='SELECT ?s ?p ?o WHERE { ?s ?p ?o . }'
  ```