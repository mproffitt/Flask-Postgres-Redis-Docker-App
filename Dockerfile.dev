FROM python:alpine 

WORKDIR /docker-flask-app

RUN apk update && apk add --no-cache\
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python", "src/app/app.py"]