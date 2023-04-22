from fastapi import APIRouter, Request
from lib.pinecone.search import answer_query

router = APIRouter()


@router.get("/")
async def query_index(request: Request):
    print('Hello world!')
    return 'Hello World'
