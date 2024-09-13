from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate


class Bot:
    def __init__(self, model_name, vectors):
        self.model_name = model_name
        self.temperature = 0
        self.vectors = vectors
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

    qa_template = """
            You are a helpful AI assistant named  MorBot. You are a virtual assistant answering questions about problems at mor software company
            Please answer the questions with the data in the database
            If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
            If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
            Use as much detail as possible when responding.
            Answer questions on Vietnamese.
            context: {context}
            Combine the chat history and follow up question into
            a standalone question. Chat History: {chat_history}"
            Follow up question: {question}
            ======
            """

    QA_PROMPT = PromptTemplate.from_template(template=qa_template)

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        # llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()
        memory = ConversationSummaryMemory(
            llm=self.llm, memory_key="chat_history", return_messages=True
        )
        chain = ConversationalRetrievalChain.from_llm(llm=self.llm,
                                                      retriever=retriever,
                                                      memory=memory,
                                                      verbose=True,
                                                      combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})
        # chain = self.QA_PROMPT | llm

        return chain(query)['answer']


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result
