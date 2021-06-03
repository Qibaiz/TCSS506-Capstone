FROM python:3.9-slim-buster
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
WORKDIR /app
CMD ["python3", "/app/wsgi.py"]