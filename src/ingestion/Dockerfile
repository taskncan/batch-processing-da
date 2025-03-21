FROM python:3.8-slim

RUN apt-get update && apt-get install -y gcc build-essential && apt-get clean

WORKDIR /app

# Copy unified requirements from project root
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ingestion source code
COPY src/ingestion/ /app

CMD ["python", "ingestion_service.py"]