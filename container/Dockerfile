# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable for CSV output path
ENV CSV_OUTPUT_PATH /output/nickel_us_gradetonnage_with_top_deposits.csv

# Run python script
CMD ["python", "sparql_gt.py", "/output/nickel_us_gradetonnage_with_top_deposits.csv"]
