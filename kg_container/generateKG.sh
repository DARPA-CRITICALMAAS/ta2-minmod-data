#!/bin/bash

# Define usage function
display_help() {
    echo "Usage: $0 [ARGUMENT1] [ARGUMENT2] [ARGUMENT3] ..."
    echo "This script generates a ttl from input data"
    echo "Arguments:"
    echo "  ARGUMENT1: type of CDR - string = 'github' or 'CDR' / help (-h)"
    echo "  ARGUMENT2: Location of CDR data = 'repo_location'or 'CDR_location'"
    echo "  ARGUMENT3: auth token if needed"
    echo "  ARGUMENT4: Master folder whose subdirectories has data - data/ for github"
    echo "  ARGUMENT5: set to 1 if file needs to be deployed"
    echo " docker run -e param1=github -e param2='https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data' -e param3=abc -e param4=data/ -e param5=1  -v /tmp:/app/generated_data/ -d -p 3030:3030 container_ttl_generate_and_deploy"
    }
# Check if the first argument is -h
if [ "$1" = "-h" ]; then
    # Display help message and exit
    display_help
    exit 0
fi

current_path=$(pwd)"/"

echo $current_path
mode=$1
bearer_token=$3
DATA_URL=$2
DIR_DATA=$4
LOCAL_DIR_CODE="$current_path""ta2-minmod-kg/"
DESTINATION_FOLDER="$current_path""/generated_data/"
DEPLOY_TTL=$5

mkdir -p "$DESTINATION_FOLDER""entities/sameAs/"
mkdir -p "$DESTINATION_FOLDER""entities/commodities/"
mkdir -p "$DESTINATION_FOLDER""entities/depositTypes/"
mkdir -p "$DESTINATION_FOLDER""entities/units/"
mkdir -p "$DESTINATION_FOLDER""json_files/umn/"
mkdir -p "$DESTINATION_FOLDER""json_files/inferlink/"
mkdir -p "$DESTINATION_FOLDER""json_files/usc/"
mkdir -p "$DESTINATION_FOLDER""json_files/sri/"
mkdir -p "$DESTINATION_FOLDER""json_files/sri/mappableCriteria"
mkdir -p "$DESTINATION_FOLDER""ttl_files/merged_ttl"
mkdir -p "$DESTINATION_FOLDER""ttl_files/umn/"
mkdir -p "$DESTINATION_FOLDER""ttl_files/inferlink/"
mkdir -p "$DESTINATION_FOLDER""ttl_files/usc/"
mkdir -p "$DESTINATION_FOLDER""ttl_files/sri/"
mkdir -p "$DESTINATION_FOLDER""ttl_files/sri/mappableCriteria"

python3.11 -m venv venv

source venv/bin/activate


pip3 install requests || echo "Module already installed"
pip3 install pyshacl || echo "Module already installed"
pip3 install jsonschema || echo "Module already installed"
pip3 install validators || echo "module already installed"
pip3 install python-slugify || echo "module already installed"
git clone https://github.com/binh-vu/drepr-v2.git
pip install drepr-v2/
pip install typer==0.9.0 || echo "module already installed"


ENTITIES="entities/"
COMMODITIES="commodities/"
DEPOSIT="depositTypes/"
UNITS="units/"
SAMEAS="sameAs/"
UMN="umn"
SRI="sri"
USC="usc/"
INFERLINK="inferlink/"
VALIDATORS="validators/"
GENERATOR="generator/"
TTL_FILES="ttl_files/"
JSON_VALIDATOR="generate_file_with_id.py"
TTL_VALIDATOR="validate_pyshacl_on_file.py"
TTL_MODEL_FILE="model_mineral_site.yml"
DEPLOYMENT="deployment/"
MERGE_JSON="merge_jsons.py"
MERGE_JSON_FOLDER="json_files/"
EXTRACTIONS="extractions"
MERGEDTTL="merged_ttl/"

COMMODITIES_FILE_YML="model_commodities.yml"
COMMODITIES_FILE_CSV="minmod_commodities.csv"
COMMODITIES_FILE_TTL="minmod_commodities.ttl"

DEPOSITS_FILE_YML="model_deposits.yml"
DEPOSITS_FILE_CSV="minmod_deposit_types.csv"
DEPOSITS_FILE_TTL="minmod_deposits.ttl"

UNITS_FILE_YML="model_units.yml"
UNITS_FILE_CSV="minmod_units.csv"
UNITS_FILE_TTL="minmod_units.ttl"

SAMEAS_FILE_YML="same_as.yml"
SAMEAS_FILE_CSV="sameas_mineralsites.csv"
SAMEAS_FILE_TTL="same_as.ttl"
# Change to the local directory


# Logic to get code files remains same

LOCAL_DIR_CODE="$current_path""ta2-minmod-kg/"

if [ -d "$LOCAL_DIR_CODE" ]; then
    cd "$current_path"
else
    git clone https://github.com/DARPA-CRITICALMAAS/ta2-minmod-kg.git "$current_path""ta2-minmod-kg"
fi

cd $LOCAL_DIR_CODE

git reset --hard HEAD
git clean -fd
git pull
git checkout delete-data-branch
git pull origin delete-data-branch

LOCAL_DIR_DATA=""
# Logic changes here based on CDR. But copy the data in local and then go from here

if [ "$mode" == "github" ]; then
    # Actions for 'github' mode
    cd "$current_path"
    LOCAL_DIR_DATA_GIT="$current_path""ta2-minmod-data/"
    echo $LOCAL_DIR_DATA_GIT
    if [ -d "$LOCAL_DIR_DATA_GIT" ]; then
        cd "$LOCAL_DIR_DATA_GIT"
    else
        echo "Clone this data"
        # Directory doesn't exist, clone the repository
        git clone https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data.git "$current_path""ta2-minmod-data"
    fi

    cd $LOCAL_DIR_DATA_GIT
    git reset --hard HEAD
    git clean -fd
    git pull
    git checkout test-blaze
    git fetch origin
    git merge test-blaze

    LOCAL_DIR_DATA="$LOCAL_DIR_DATA_GIT""$DIR_DATA"
else

    # Actions for other modes
    # Not Implemented yet
    echo "Performing actions for other modes"
    # Add your other mode-specific actions here
fi

echo $LOCAL_DIR_DATA

#Commodities
python3 -m drepr $LOCAL_DIR_CODE$GENERATOR$ENTITIES$COMMODITIES$COMMODITIES_FILE_YML default=$LOCAL_DIR_DATA$ENTITIES$COMMODITIES$COMMODITIES_FILE_CSV > $DESTINATION_FOLDER$ENTITIES$COMMODITIES$COMMODITIES_FILE_TTL

#Deposit Types
python3 -m drepr $LOCAL_DIR_CODE$GENERATOR$ENTITIES$DEPOSIT$DEPOSITS_FILE_YML default=$LOCAL_DIR_DATA$ENTITIES$DEPOSIT$DEPOSITS_FILE_CSV > $DESTINATION_FOLDER$ENTITIES$DEPOSIT$DEPOSITS_FILE_TTL
#Units
python3 -m drepr $LOCAL_DIR_CODE$GENERATOR$ENTITIES$UNITS$UNITS_FILE_YML default=$LOCAL_DIR_DATA$ENTITIES$UNITS$UNITS_FILE_CSV > $DESTINATION_FOLDER$ENTITIES$UNITS$UNITS_FILE_TTL
#SameAs Files
nickel_sames='nickel_sameas.csv'
tungsten_sames='tungsten_sameas.csv'
NICKEL_TTL='nickel_sameas.ttl'
TUNGSTEN_TTL='tungsten_sameas.ttl'

python3 -m drepr $LOCAL_DIR_CODE$GENERATOR$ENTITIES$SAMEAS$SAMEAS_FILE_YML default=$LOCAL_DIR_DATA$DATA$UMN"/sameas/"$nickel_sames > $DESTINATION_FOLDER$ENTITIES$SAMEAS$NICKEL_TTL

python3 -m drepr $LOCAL_DIR_CODE$GENERATOR$ENTITIES$SAMEAS$SAMEAS_FILE_YML default=$LOCAL_DIR_DATA$DATA$UMN"/sameas/"$tungsten_sames > $DESTINATION_FOLDER$ENTITIES$SAMEAS$TUNGSTEN_TTL

##Validate json in all files in inferlink folder

# Path to the folder containing files
folder_path_inferlink="$LOCAL_DIR_DATA$INFERLINK$EXTRACTIONS"
folder_path_umn="$LOCAL_DIR_DATA$UMN"
json_script_path="$LOCAL_DIR_CODE$VALIDATORS$JSON_VALIDATOR"


json_files_path="$DESTINATION_FOLDER$MERGE_JSON_FOLDER"
folder_path_inferlink_id="$json_files_path$INFERLINK"

#First delete any existing file

 find $folder_path_inferlink_id -type f -exec rm {} \;
 for file_path in "$folder_path_inferlink"/*; do
     if [ -f "$file_path" ]; then
         echo $file_path
         python3 "$json_script_path" "$file_path" "$folder_path_inferlink_id"
         if [ $? -ne 0 ]; then
             echo "python3 script failed"
         fi
     fi
 done


## Validate SRI as well
folder_path_sri="$LOCAL_DIR_DATA$SRI"
folder_path_sri_id="$json_files_path$SRI"

#First delete any existing file
find $folder_path_sri_id -type f -exec rm {} \;
for file_path in "$folder_path_sri"/*; do
   if [ -f "$file_path" ]; then
       echo $file_path
       python3 "$json_script_path" "$file_path" "$folder_path_sri_id"
       if [ $? -ne 0 ]; then
           echo "Validate json script failed"
       fi
   fi
done

## Validate UMN as well

folder_path_umn_id="$json_files_path$UMN"
find $folder_path_umn_id -type f -exec rm {} \;
for file_path in "$folder_path_umn"/*; do
    if [ -f "$file_path" ]; then
        echo $file_path
        python3 "$json_script_path" "$file_path" "$folder_path_umn_id"
        if [ $? -ne 0 ]; then
            echo "Validate json script failed"
        fi
    fi
done

## Validate SRI MC as well

folder_path_sri_mc="$LOCAL_DIR_DATA$SRI""/""mappableCriteria"
folder_path_sri_mc_id="$json_files_path$SRI""/""mappableCriteria"
drepr_yaml_path="$LOCAL_DIR_CODE""generator/$TTL_MODEL_FILE"
drepr_yaml_path_mc="$LOCAL_DIR_CODE""generator/""model_mineral_system_v2.yml"


#First delete any existing file

find $folder_path_sri_mc_id -type f -exec rm {} \;
echo $folder_path_sri_mc
file_list_sri_mc=""

for file_path in "$folder_path_sri_mc"/*; do
    # Check if the item is a file (not a directory)
    if [ -f "$file_path" ]; then
        echo $file_path
        # Run the python3 script on the current file
        python3 "$json_script_path" "$file_path" "$folder_path_sri_mc_id"
        if [ $? -ne 0 ]; then
            echo "Validate json script failed"
            # Replace by say an email or some call to inform someone
        fi
    fi
done


final_file="$DESTINATION_FOLDER$TTL_FILES""final_kg_file.ttl"

# Create ttl file from all files in sri folder
save_ttl_files_path_sri="$DESTINATION_FOLDER$TTL_FILES$SRI""/"
find $save_ttl_files_path_sri -type f -exec rm {} \;
file_list_sri=""
for file_path in "$folder_path_sri_id"/*; do
   if [ -f "$file_path" ]; then
       filename=$(basename "$file_path")
       filename_no_ext="${filename%.*}"
       generated_ttl_path="$save_ttl_files_path_sri$filename_no_ext"".ttl"
       echo $generated_ttl_path
       drepr_command='python3 -m drepr "$drepr_yaml_path" default="$file_path"'
       echo "Running command: $drepr_command"
       eval "$drepr_command" > "$generated_ttl_path"
       cat $generated_ttl_path >> $final_file
	       file_list_sri="$file_list_sri $generated_ttl_path"
       if [ $? -ne 0 ]; then
           echo "python3 script failed"
       fi
   fi
done

# Create ttl file from all files in sri mc folder
save_ttl_files_path_sri_mc="$DESTINATION_FOLDER$TTL_FILES$SRI""/""mappableCriteria"
find $save_ttl_files_path_sri_mc -type f -exec rm {} \;
file_list_sri_mc=""
for file_path in "$folder_path_sri_mc_id"/*; do
    if [ -f "$file_path" ]; then
        filename=$(basename "$file_path")
        filename_no_ext="${filename%.*}"
        generated_ttl_path="$save_ttl_files_path_sri_mc/""$filename_no_ext"".ttl"
        echo $generated_ttl_path
        drepr_command='python3 -m drepr "$drepr_yaml_path_mc" default="$file_path"'
        echo "Running command: $drepr_command"
        eval "$drepr_command" > "$generated_ttl_path"
	    file_list_sri_mc="$file_list_sri_mc $generated_ttl_path"
        if [ $? -ne 0 ]; then
            echo "python3 script failed"
        fi
    fi
done


## Create ttl file from all files in inferlink folder

save_ttl_files_path="$DESTINATION_FOLDER$TTL_FILES$INFERLINK"
find $save_ttl_files_path -type f -exec rm {} \;
file_list_inferlink=""
for file_path in "$folder_path_inferlink_id"/*; do
     if [ -f "$file_path" ]; then
         filename=$(basename "$file_path")
         filename_no_ext="${filename%.*}"
         generated_ttl_path="$save_ttl_files_path$filename_no_ext"".ttl"
         echo $generated_ttl_path
         drepr_command='python3 -m drepr "$drepr_yaml_path" default="$file_path"'
         echo "Running command: $drepr_command"
         eval "$drepr_command" > "$generated_ttl_path"
         cat $generated_ttl_path >> $final_file

 	      file_list_inferlink="$file_list_inferlink "$generated_ttl_path""
         if [ $? -ne 0 ]; then
             echo "python3 script failed"
         fi
     fi
 done


# Create ttl file from all files in umn folder

save_ttl_files_path_umn="$DESTINATION_FOLDER$TTL_FILES$UMN""/"
find $save_ttl_files_path_umn -type f -exec rm {} \;
file_list_umn=""
for file_path in "$folder_path_umn_id"/*; do
    if [ -f "$file_path" ]; then
        filename=$(basename "$file_path")
        filename_no_ext="${filename%.*}"
        generated_ttl_path="$save_ttl_files_path_umn$filename_no_ext"".ttl"
        echo $generated_ttl_path
        drepr_command='python3 -m drepr "$drepr_yaml_path" default="$file_path"'
        echo "Running command: $drepr_command"
         eval "$drepr_command" > "$generated_ttl_path"
	    file_list_umn="$file_list_umn $generated_ttl_path"
        if [ $? -ne 0 ]; then
            echo "python3 script failed"
        fi
    fi
done

## Create ttl file from all files in usc folder
save_ttl_files_path_usc="$LOCAL_DIR_DATA$USC"
file_list_usc=""
for file in "$save_ttl_files_path_usc"/*; do
   if [ -f "$file" ]; then
       file_list_usc="$file_list_usc $file"
       cat $file >> $final_file
   fi
done


cat "$DESTINATION_FOLDER$ENTITIES$COMMODITIES$COMMODITIES_FILE_TTL" >> "$final_file"

cat "$DESTINATION_FOLDER$ENTITIES$DEPOSIT$DEPOSITS_FILE_TTL" >> "$final_file"

cat "$DESTINATION_FOLDER$ENTITIES$UNITS$UNITS_FILE_TTL" >> "$final_file"

cat $DESTINATION_FOLDER$ENTITIES$SAMEAS$NICKEL_TTL >> "$final_file"
cat $DESTINATION_FOLDER$ENTITIES$SAMEAS$TUNGSTEN_TTL >> "$final_file"

deactivate
# Check if the first argument is -h
if [ "$DEPLOY_TTL" = "1" ]; then
  cd $current_path

  if [ -f "apache-jena-fuseki-5.0.0.tar.gz" ]; then
    echo "File apache-jena-fuseki-5.0.0.tar.gz already exists in the current directory."
  else
    # Perform actions if the file does not exist
    wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.0.0.tar.gz
    tar -xzvf apache-jena-fuseki-5.0.0.tar.gz
  fi

  cd $current_path"/apache-jena-fuseki-5.0.0"
  fuser -k 3030/tcp
  ./fuseki-server --file "$final_file"  /minmod

fi

