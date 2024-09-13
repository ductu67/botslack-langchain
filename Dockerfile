FROM python:3.10

EXPOSE 8118
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python3", "emdedder.py"]

CMD [ "python3", "slack_bot.py"]