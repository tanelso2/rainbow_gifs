FROM python:3

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=app

COPY ./*.py ./

COPY templates ./templates/

COPY static ./static/

EXPOSE 5000

RUN mkdir -p static/images/output

CMD gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
