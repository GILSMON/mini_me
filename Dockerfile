FROM python:3.12-slim

WORKDIR /app

# Install deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data
COPY app/ app/
COPY data/ data/

# Ingest biography into ChromaDB at build time
# (vectors baked into the image — no runtime API call needed for ingestion)
RUN python -m app.ingest

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
