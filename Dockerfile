FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Definindo workers, threads e timeout
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "300"]