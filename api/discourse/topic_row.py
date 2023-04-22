import asyncio
import time


async def topic_row(discourse_url: str, topic_json: dict, category_id_to_name: dict) -> str:
    topic_url = f"{topic_json['slug']}/{topic_json['id']}"
    topic_title_text = topic_json['fancy_title']
    topic_post_count = topic_json['posts_count']

    topic_html = f"""
        Category: {category_id_to_name}
        Topic Url: {topic_url}
        Title: {topic_title_text}
        Post count: {topic_post_count}
    """

    await asyncio.sleep(0.5)
    return topic_html
