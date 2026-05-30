FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

COPY . .
EXPOSE 8000

# Must be api.main:app not main:app because main.py is inside the api/ folder
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]