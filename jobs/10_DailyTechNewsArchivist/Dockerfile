# Use the lightweight Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Install system-level dependencies required for compiling 'lxml'
# 'lxml' is a C-based library, so it needs 'gcc' and development headers (libxml2-dev, libxslt-dev)
# We clean up the apt cache afterwards to keep the image size small
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libxml2-dev \
#     libxslt-dev \
#     && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version to avoid installation issues
RUN pip install --upgrade pip

# Install the required Python libraries
RUN pip install requests beautifulsoup4 lxml

# Copy the scraper script from the host to the container
COPY scraper.py .

# Create a directory to store the output files (CSV/HTML)
RUN mkdir data

# Define the default command to execute the scraper when the container starts
CMD ["python", "scraper.py"]