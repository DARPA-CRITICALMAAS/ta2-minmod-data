#!/bin/bash

# Define usage function
display_help() {
    echo "Usage: $0 [ARGUMENT1] [ARGUMENT2] [ARGUMENT3] ..."
    echo "This script deploys a ttl from input data"
    echo "Arguments:"
    echo "  ARGUMENT1: ttl file path + name"
}
# Check if the first argument is -h
if [ "$1" = "-h" ]; then
    # Display help message and exit
    display_help
    exit 0
fi

echo "My variable value is: $TTL"


current_path=$(pwd)"/"

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
./fuseki-server --file "$current_path$TTL"  /minmod

fi

