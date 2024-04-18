# Use the latest Ubuntu base image
FROM ubuntu:latest

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y python3.11 && \
    apt-get install -y python3.11-venv && \
    apt-get install -y python3.11 wget && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update

# Set the working directory in the container
WORKDIR /app

# Copy the shell script into the container
COPY generateKG.sh /app/

# Set execute permissions for the script
RUN chmod +x generateKG.sh

ENV param1=github
ENV param2=https://github.com/DARPA-CRITICALMAAS/ta2-minmod-data
ENV param3=abc
ENV param4=data/
ENV param5=/generated_data
ENV param6=/ttl_data/
ENV param7=/ttl_data/same_as.ttl


# Define the command to run the script when the container starts
CMD ["sh", "-c",  "./generateKG.sh ${param1} ${param2} ${param3} ${param4} ${param5} ${param6} ${param7}"]