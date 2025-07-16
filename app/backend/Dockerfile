# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file first to leverage Docker's build cache
COPY ./requirements.txt /code/requirements.txt

# Install the Python packages needed for the application
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application's code from your computer into the container
COPY . /code

# The command to run when the container starts.
# It runs Uvicorn on host 0.0.0.0 to make it accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]