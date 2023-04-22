import asyncio
import httpx
import json

from typing import List, Dict, Any
from config import settings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .get_topic_content import get_topic_content
from .topic_row import topic_row
from lib.pinecone.ingest import insert_into_index


def flatten_and_join(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_and_join(item))
        else:
            result.append(item)
    return result

# Throttled function to fetch topic content


async def get_throttled_topic_content(discourse_url, topic):
    # logging.info(topic)
    await asyncio.sleep(0.2)  # Wait for 200ms before making a request
    return await get_topic_content(discourse_url, topic)


async def fetch_all_topics(discourse_url, topic_list):
    content = []
    for topic in topic_list:
        try:
            topic_content = await get_throttled_topic_content(discourse_url, topic)
            content.append(topic_content)
        except Exception as error:
            print(f"Error occurred while fetching topic {topic}: {error}")
    return content


async def content_chunks(contents: str):
    print(type(contents))
    raw_docs = Document(page_content=contents)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    return text_splitter.split_documents([raw_docs])


async def process_discourse(topic_list: List[Dict[str, Any]], discourse_url: str, openai_api_key: str, namespace=""):
    try:
        content = await fetch_all_topics(discourse_url, topic_list)
        flat_content = [item for sublist in content for item in sublist]

        category_url = f"{discourse_url}/categories.json"
        async with httpx.AsyncClient(max_redirects=5) as client:
            response = await client.get(category_url)
            categories = response.json()["category_list"]["categories"]
            category_id_to_name = {cat["id"]: cat["name"]
                                   for cat in categories}

        topic_rows = await asyncio.gather(*[topic_row(discourse_url, topic, category_id_to_name) for topic in topic_list])
        rows = " ".join(topic_rows)
        contents = json.dumps(flat_content)
        contentSum = rows + contents

        resolved_content_chunks = await content_chunks(contentSum)

        insert_into_index(resolved_content_chunks, namespace=namespace,
                          openai_api_key=openai_api_key)
        await asyncio.sleep(0.5)
        return
    except Exception as error:
        raise error
