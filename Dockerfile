FROM python:3

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=app

COPY ./*.py ./

COPY templates ./templates/

EXPOSE 5000

RUN mkdir -p static/output/

CMD flask run --host=0.0.0.0
