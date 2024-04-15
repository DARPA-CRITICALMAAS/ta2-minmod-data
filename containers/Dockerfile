# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# define an environment variable for the commodity (with default value as nickel)
ENV COMMODITY=nickel

# Run python script using the environment variable
CMD ["sh", "-c", "python generate_ta2_outputs.py --commodity ${COMMODITY} --output_directory /output/"]
