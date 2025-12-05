
FROM python:3.12-alpine3.20

RUN pip install --no-cache-dir pip

WORKDIR /app_root

COPY ./app /app_root/app
COPY requirements.txt /app_root/

WORKDIR /app_root

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
