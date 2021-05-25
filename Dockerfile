FROM python:3.9-slim-buster
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /app
CMD ["python3", "/app/run.py"]