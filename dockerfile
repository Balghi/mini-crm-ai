# --- STAGE 1: The Builder ---
# This stage installs dependencies into a virtual environment.
FROM python:3.11 as builder

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the requirements file
COPY requirements.txt .

# Install CPU-only PyTorch FIRST, then the rest of the requirements.
# This is the key to reducing the image size.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt


# --- STAGE 2: The Final Image ---
# This stage creates the small, final image for production.
FROM python:3.11-slim as final

WORKDIR /app

# Copy the virtual environment from the builder stage.
# This contains all our installed packages but none of the build bloat.
COPY --from=builder /venv /venv

# Copy the application code
COPY . .

# Set the PATH to include our virtual environment's binaries
ENV PATH="/venv/bin:$PATH"