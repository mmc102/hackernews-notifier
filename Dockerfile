# Use a lightweight Python image
FROM python:3.10-slim

# Install dependencies
RUN pip install requests python-telegram-bot sqlite3

# Add the script to the container
COPY hackernews_checker.py /app/hackernews_checker.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "hackernews_checker.py"]
