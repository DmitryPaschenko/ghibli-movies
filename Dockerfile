FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
CMD ["celery", "-A", "tasks", "beat", "--loglevel=info"]
CMD ["python", "app.py"]