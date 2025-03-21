FROM python:3.8-slim

RUN apt-get update && apt-get install -y gcc build-essential && apt-get clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the delivery source code
COPY src/delivery/ /app

CMD ["python", "api_service.py"]