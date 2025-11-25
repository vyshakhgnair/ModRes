FROM python:3.9-slim

# Install system dependencies + Tectonic
RUN apt-get update && apt-get install -y \
    libssl-dev \
    curl \
    && curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
    && mv tectonic /usr/local/bin/ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App
COPY . .

# Create output directory for PDFs
RUN mkdir -p output

# Run Command
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:10000", "app:app"]
