## Run the whole pipeline using Docker

Docker allows an isolated OS-level virtualization and thus a completely separate environment in which you can run the whole process without performing any additional installations on your machine.

### Option 1
Building the image manually:
```
docker build -t container_minmod_grade_tonnage .
```

### Option 2
Pull the image from Docker-Hub:
```
docker pull nemo1012/container_minmod_grade_tonnage
```

### Running the container
To generate the file in the <hostmachine_volume>, run the following command:
```
docker run -v <hostmachine_volume>:/output container_minmod_grade_tonnage
```
For example:
```
 docker run -v /Users/namratasharma/Documents:/output container_minmod_grade_tonnage
```
Make sure that:
1. The volume you are using (on your local machine) has 'File Sharing' enabled in the Docker settings
2. You are using full paths (on both the local machine and the docker container)
3. The user running the docker command has access privlege (can be done by `sudo chmod 777 <hostmachine_volume>`)

If you have pulled the image from Docker hub, the following command can be run:
```
docker run -v <hostmachine_volume>:/output nemo1012/container_minmod_grade_tonnage
```
For example:
```
 docker run -v /Users/namratasharma/Documents:/output nemo1012/container_minmod_grade_tonnage
```
------------------
