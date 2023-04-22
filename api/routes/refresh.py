from fastapi import HTTPException, Request, APIRouter
import httpx
from constants import communities
import json.decoder
from logger import logger

from api.discourse.main import process_discourse

router = APIRouter()

# TODO: Define what's the max number of topics to process
max_more_topics = 5


@router.post("/refresh")
async def handler(request: Request):
    req = await request.json()
    credentials = req['credentials']
    openai_api_key = credentials['openaiApiKey']
    status = "success"

    community_name = credentials["community"]["name"] if credentials["community"] else None
    if not community_name:
        raise HTTPException(
            status_code=500, detail="No community URL provided.")

    try:
        cnt = 0
        discourse_url = communities[community_name]["discourse_url"]
        topic_path = "/latest.json?no_definitions=true&page="
        base_topic_url = discourse_url + topic_path
        url = base_topic_url + str(cnt)

        async with httpx.AsyncClient(max_redirects=5) as client:
            try:
                topic_response = await client.get(url)
                topic_response.raise_for_status()
            except httpx.RequestError as e:
                print(f"HTTP GET error: {str(e)}")
            except httpx.HTTPError as e:
                print(f"HTTP error: {str(e)}")
            except httpx.TimeoutException as e:
                print(f"Request timed out: {str(e)}")
            except json .decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {str(e)}")

            json_response = topic_response.json()
            topic_list = json_response["topic_list"]["topics"]
            await process_discourse(topic_list, discourse_url, openai_api_key, namespace=community_name)

            while (
                "more_topics_url" in json_response["topic_list"] and cnt < max_more_topics
            ):
                print(f"cnt is {cnt}\n============")
                cnt += 1
                url = base_topic_url + str(cnt)
                new_response = await client.get(url)

                new_topic_list = new_response.json()["topic_list"]["topics"]
                await process_discourse(new_topic_list[1:], discourse_url, openai_api_key, namespace=community_name)

        return {"status": status}
    except Exception as e:
        logger.exception("An error occurred")
        raise HTTPException(status_code=500, detail=str(e) or "Unknown error.")
