FROM python:3.9

RUN mkdir usr/app
WORKDIR usr/app

RUN mkdir images

WORKDIR images

RUN mkdir posts

RUN mkdir users

WORKDIR ..

COPY . .

RUN pip install -r requirements.txt

CMD python app.py