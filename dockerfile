# Dockerfile (FINAL, MOST ROBUST VERSION V2)

# --- STAGE 1: The Builder ---
# This stage installs dependencies into a virtual environment.
FROM python:3.11 as builder

# Install system-level build tools. This is needed to compile psycopg2 from source.
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the requirements file
COPY requirements.txt .

# Upgrade pip to ensure we have the latest dependency resolver
RUN pip install --upgrade pip

# Install all packages in a single, robust command.
# --extra-index-url adds the PyTorch CPU repo as an additional source,
# allowing pip to resolve all dependencies from PyPI and the CPU-only repo at once.
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu


# --- STAGE 2: The Final Image ---
# This stage creates the small, final image for production.
FROM python:3.11-slim as final

# Install the PostgreSQL runtime client library.
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment from the builder stage.
COPY --from=builder /venv /venv

# Copy the application code
COPY . .

# Set the PATH to include our virtual environment's binaries
ENV PATH="/venv/bin:$PATH"