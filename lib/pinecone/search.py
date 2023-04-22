from langchain.llms import OpenAI
# from langchain.vectorstores import Pinecone
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from config import settings
import pinecone
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import BaseMessage
from typing import Union, Tuple


def dict_to_chat_turn(data: dict) -> Union[Tuple[str, str], BaseMessage]:
    if "query" in data and "answer" in data:
        return (data["query"], data["answer"])
    else:
        raise ValueError("Unsupported dictionary format")


def answer_query(query="", openai_api_key=None, history=[], chain_type="stuff", temperature=0.5, namespace=""):
    llm = OpenAI(temperature=temperature,
                 openai_api_key=openai_api_key, model_name="gpt-4")
    chain = load_qa_chain(llm, chain_type=chain_type)

    # initialize pinecone
    pinecone.init(
        api_key=settings.pinecone_api_key,  # find at app.pinecone.io
        environment=settings.pinecone_environment  # next to api key in console
    )
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    docsearch = Pinecone.from_existing_index(
        index_name=settings.pinecone_index, embedding=embeddings, namespace=namespace)

    qa = ConversationalRetrievalChain.from_llm(
        llm, docsearch.as_retriever(), return_source_documents=True)
    formatted_history = [dict_to_chat_turn(turn) for turn in history]
    result = qa({"question": query, "chat_history": formatted_history})

    return result["answer"]
