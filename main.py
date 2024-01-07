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

def write_content(label):
    if label == "MBTI":
        response = ai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": USER}
                ],
                temperature=1,
                stream=True
            )

    writing = ""
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta'].keys():
            writing += chunk['choices'][0]['delta']['content']
            print(chunk['choices'][0]['delta']['content'], end="")
    print("")
    return writing

def get_hashtag(writing):
    response = ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": writing},
                {"role": "user", "content": """위 블로그 글과 맞는 해시 태그 만들어줘. 쉼표로 구분하고 #제거
해쉬 태그:"""}
                ],
            temperature=0,
        )
    return response['choices'][0]['message']['content']

def sep_writing(writing):
    title = writing[4:writing.find('\n')]
    content = writing[writing.find('<'):]
    return title, content
if __name__ == "__main__":
    label = "MBTI"
    category = get_category_id(label)
    writing = write_content(label)
    title, content = sep_writing(writing)
    print("title: " + title)
    print(content)
    tag = get_hashtag(writing)
    print(tag)
    write_blog(title, content, category, tag)
    