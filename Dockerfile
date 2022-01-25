# pull official base image
FROM python:3.8.12

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN apt-get install netcat -y

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN apt-get install dos2unix && dos2unix ./entrypoint.sh
RUN sed -i -e 's/\r$//' ./entrypoint.sh
RUN chmod u+x ./entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["bash","entrypoint.sh"]


    

