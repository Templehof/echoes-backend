FROM python:3.14.0b3-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /app/src

WORKDIR /app/src

CMD ["fastapi", "run", "main.py", "--port", "80", "--proxy-headers"]