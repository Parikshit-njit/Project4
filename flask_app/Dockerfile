FROM python:3.8

EXPOSE 5000

WORKDIR /flask_app

COPY requirements.txt /flask_app
RUN pip install -r requirements.txt

COPY . /flask_app

CMD python3 -m  app