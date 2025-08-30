# Use an official Python 3.9 image as our base
FROM python:3.11-slim

# This is the crucial step: Install the Tesseract OCR program onto the server's operating system
RUN apt-get update && apt-get install -y tesseract-ocr

# Set the working directory inside our server
WORKDIR /app

# Copy the shopping list (requirements.txt) into the server
COPY requirements.txt .

# Install all the Python libraries from the shopping list
RUN pip install --no-cache-dir -r requirements.txt

# Copy all of your project files (app.py, static/, templates/) into the server
COPY . .

# Tell the world that our application will be available on port 10000
EXPOSE 10000

# The command to start your application when the server turns on
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]