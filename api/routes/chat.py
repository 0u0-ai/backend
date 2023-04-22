from fastapi import APIRouter, Request
from lib.pinecone.search import answer_query

router = APIRouter()


@router.post("/chat")
async def query_index(request: Request):
    req = await request.json()
    credentials = req['credentials']
    history = req['chatHistory']
    question = req['question']
    status = "success"

    openai_api_key = credentials['openaiApiKey']

    generated_response = answer_query(
        query=question, openai_api_key=openai_api_key, history=history)
    print(generated_response)
    return {"answer": generated_response, status: status}
