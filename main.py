import requests as r
import openai as ai
import os
from config import *
from dotenv import load_dotenv

load_dotenv(verbose=True)

ai.api_key = os.getenv('GPT_API_KEY')
access = os.getenv('ACCESS_TOKEN')

def write_blog(title, content, category, tag):
    url = "https://www.tistory.com/apis/post/write"
    params = {
            "access_token": access,
            "blogName": "giftedmbti",
            "title": title,
            "content": content,
            "visibility": 0,
            "category": category,
            "tag": tag,
            "output": "json"
    }
    r.post(url=url, params=params)

def get_category_id(label):
    url = "https://www.tistory.com/apis/category/list"
    params = {
            "access_token": access,
            "blogName": "essaywrit",
            "output": "json"
            }
    category = r.get(url=url, params=params).json()
    for i in category['tistory']['item']['categories'] :
        if i['label'] == label:
            return i['id']

def process_and_write_content(label, specific_MBTI):
    category = get_category_id(label)
    writing = write_content(label, specific_MBTI)
    title, content = sep_writing(writing)
    print("title: " + title)
    print(content)
    tag = get_hashtag(writing)
    print(tag)
    write_blog(title, content, category, tag)

if __name__ == "__main__":
    mbti_types = ["ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP",
                  "INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP"]

    for mbti_type in mbti_types:
        label = "MBTI"
        specific_MBTI = mbti_type
        process_and_write_content(label, specific_MBTI)

