FROM python:3.9-slim

WORKDIR /app

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn" , "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
