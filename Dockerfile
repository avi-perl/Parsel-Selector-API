FROM python:3.7

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
