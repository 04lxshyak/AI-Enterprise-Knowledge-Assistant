# Base image with Python + uv
FROM astral/uv:python3.12-bookworm-slim

# Optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy source code
COPY app ./app

# Render passes this variable automatically (PORT)
ENV PORT=8000

# Document the port
EXPOSE ${PORT}

# Command to run FastAPI in production
CMD uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
