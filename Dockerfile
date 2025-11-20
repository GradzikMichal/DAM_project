FROM python:3.12-slim AS builder
LABEL authors="Michal"
RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY django_web /app/
COPY kafka_setup.py /app/
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
#RUN python kafka_setup.py
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD python kafka_setup.py; python manage.py runserver 0.0.0.0:8000
