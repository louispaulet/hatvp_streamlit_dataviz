# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN chmod -R 777 .


# Expose the port that Streamlit runs on
EXPOSE 8501

# Run Streamlit when the container starts
CMD ["streamlit", "run", "main.py"]