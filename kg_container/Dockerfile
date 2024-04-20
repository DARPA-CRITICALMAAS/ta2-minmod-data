# Use the Ubuntu in VM
FROM ubuntu:20.04


# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y git python3.11 python3.11-venv python3-pip wget openjdk-17-jdk && \
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
ENV param5=0

# Define the command to run the script when the container starts
CMD ["sh", "-c",  "./generateKG.sh ${param1} ${param2} ${param3} ${param4} ${param5} ${param6} ${param7} ${param8}"]