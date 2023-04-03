FROM python:3.8
RUN pip install --upgrade pip
RUN pip install django-cors-headers
RUN pip3 install psycopg2-binary
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
