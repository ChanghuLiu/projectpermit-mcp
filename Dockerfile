FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data
RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

EXPOSE 8000
CMD ["sh", "-c", "uvicorn projectpermit.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
