FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /ChannelsBot

WORKDIR /ChannelsBot

COPY web/requirements.txt /ChannelsBot/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /ChannelsBot/

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "ChannelsBot.wsgi:application"]
