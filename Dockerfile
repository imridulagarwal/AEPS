FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl xvfb libxi6 libgconf-2-4 libnss3 libxss1 libappindicator1 libindicator7 \
    fonts-liberation libatk-bridge2.0-0 libgtk-3-0 libxrandr2 libasound2 libpangocairo-1.0-0 \
    libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxinerama1 libpangoft2-1.0-0 \
    chromium chromium-driver

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/lib/chromium/

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start app
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
