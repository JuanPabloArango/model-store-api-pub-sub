FROM python:3.10

EXPOSE 8080

COPY . /app
COPY requirements.txt .

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["flask", "db", "upgrade", "&&", "python", "subscriber.py"]