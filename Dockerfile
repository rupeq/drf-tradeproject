FROM python:3.8.5

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

COPY entrypoint.sh /code/
RUN chmod +x entrypoint.sh

RUN pip3 install -r requirements.txt
