FROM python:3.11

RUN mkdir app

COPY ./requirements.txt /app/requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh

COPY .  /app/

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir  -r requirements.txt

WORKDIR /app

EXPOSE 8000

CMD [ "sh","entrypoint.sh" ]

