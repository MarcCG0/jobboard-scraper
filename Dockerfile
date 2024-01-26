# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"


# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r src/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run python3 runner/main.py when the container launches
CMD ["python3", "src/runner/main.py", "--location", "Barcelona", "--keywords", "ETL"]
