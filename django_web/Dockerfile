FROM python:3.13-slim AS builder
RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python app/manage.py runserver
LABEL authors="Michal"
EXPOSE 8000