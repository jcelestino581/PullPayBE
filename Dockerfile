FROM python:3.11

# Set environment variables
ENV DB_NAME=pullpaybe
ENV DB_USER=jcele
ENV DB_PASSWORD=Pooper581
ENV DB_HOST=my-postgres
ENV DB_PORT=5432

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

