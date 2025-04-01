FROM python:3.10

EXPOSE 8080

COPY . /app
COPY requirements.txt .

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]