# Step 1: Start with a pre-made box that has Python 3.9 installed.
# We use the "slim" version because it's smaller and more efficient.
FROM python:3.9-slim

# Step 2: Set the working directory inside the box to a folder named /app.
# From now on, all commands will run from inside this folder.
WORKDIR /app

# Step 3: Copy our local files into the box.
# First, copy just the requirements file.
COPY requirements.txt .

# Step 4: Run the 'pip install' command inside the box.
# This installs Flask, just like you did manually on your computer.
RUN pip install -r requirements.txt

# Step 5: Copy the rest of our project files (app.py, templates folder) into the box.
COPY . .

# Step 6: Tell the box what command to run when it starts.
# This will execute 'python app.py' to start the Flask server.
CMD ["python", "app.py"]