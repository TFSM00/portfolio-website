FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
# python run.py
CMD gunicorn --certfile /etc/nginx/certificate.crt --keyfile /etc/nginx/private.key --bind 0.0.0.0:5000 -w 4 --threads 4 --preload run:app
