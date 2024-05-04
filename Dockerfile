FROM python:3.10-alpine

COPY . /user_service
EXPOSE 8000
RUN apk update
RUN apk add libpq-dev
RUN apk add build-base
WORKDIR /user_service
RUN pip3 install -r requirements.txt
WORKDIR /user_service/users_microservice
CMD ["python","manage.py","runserver"]