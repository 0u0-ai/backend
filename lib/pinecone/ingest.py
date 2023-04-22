from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from config import settings


def insert_into_index(texts, namespace="", openai_api_key=None):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # initialize pinecone
    pinecone.init(
        api_key=settings.pinecone_api_key,  # find at app.pinecone.io
        environment=settings.pinecone_environment  # next to api key in console
    )

    index_name = settings.pinecone_index
    print(index_name)
    print(pinecone.list_indexes())
    if index_name not in pinecone.list_indexes():
        # create index only if it does not exist
        pinecone.create_index(dimension=1536, name=index_name)
    pinecone.list_indexes()

    docsearch = Pinecone.from_documents(
        texts,
        embeddings,
        index_name=index_name,
        namespace=namespace
    )

    return docsearch
