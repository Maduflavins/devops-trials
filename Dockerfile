
FROM python:3.10.0b1-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

ADD . /usr/src/app


# collect static files
RUN python manage.py collectstatic --noinput

CMD gunicorn reeach.wsgi:application --bind 0.0.0.0:$PORT
