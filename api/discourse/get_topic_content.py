import httpx


async def get_topic_content(discourse_url: str, topic_json: dict):
    topic_download_url = f"{discourse_url}/t/{topic_json['slug']}/{topic_json['id']}"

    try:
        async with httpx.AsyncClient(max_redirects=5) as client:
            response = await client.get(f"{topic_download_url}.json")
            response_json = response.json()
            posts_json = response_json["post_stream"]["posts"]
            return posts_json
    except Exception as err:
        print("in write_topic error:", "Error fetching topic" + str(err))
