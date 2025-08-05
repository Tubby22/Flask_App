# Use a more specific Python image for better security and smaller size
FROM python:3.10-slim

# Set the working directory
WORKDIR /Auth

# Copy the requirements file first to leverage Docker's build cache
COPY requirements.txt .

# Install dependencies. This step will only run again if requirements.txt changes
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's files
COPY . .

# Expose the port your application is actually running on
# Make sure your app.run() or equivalent is binding to this port
EXPOSE 5000

# Run the python file
CMD [ "python", "Authentication.py" ]