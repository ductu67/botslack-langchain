import os

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from bot import Bot
load_dotenv()
# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
vectordb = Chroma(
    client=chromadb.PersistentClient("./openai"),
    collection_name='openaiembeddings',
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002", )
)
mode_name = 'gpt-3.5-turbo'
mybot = Bot(model_name=mode_name, vectors=vectordb)


@app.event("app_mention")
def handle_message_events(body, say, logger):
    user = "<@{}>".format(body['authorizations'][0]['user_id'])
    message = body['event']['text'].replace(user, '').strip()
    answer = mybot.conversational_chat(query=message)
    say(answer)


@app.event("message")
def handle_message_events(body, say, logger):
    user = "<@{}>".format(body['authorizations'][0]['user_id'])
    message = body['event']['text'].replace(user, '').strip()
    answer = mybot.conversational_chat(query=message)
    say(answer)


# Ready? Start your app!
if __name__ == "__main__":
    a = SocketModeHandler(app, os.environ.get("SLACK_APP_SECRET"))
    a.start()
    # app.start(port=int(os.environ.get("PORT", 3000)))
