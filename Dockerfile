FROM python:slim

#Download uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Install dependencies and current package in editable mode
RUN uv sync --frozen
RUN uv pip install -e .

#Put virtual env path just created to the front 
ENV PATH="/app/.venv/bin:$PATH"

# Train model
RUN python pipeline/training_pipeline.py

EXPOSE  5000

CMD ["python", "app.py"]