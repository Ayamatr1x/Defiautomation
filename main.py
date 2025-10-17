import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

def get_trending_posts(subreddit="defi", limit=5):
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t=day"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()

        posts = []
        for post in data["data"]["children"]:
                title = post["data"]["title"]
                posts.append(title)
        return posts

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_idea(topic):
        prompt = f"Suggest a catchy tweet idea about this DeFi topic: '{topic}'. Keep it under 20 words and engaging."
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    posts = get_trending_posts()
    print("Trending DeFi Topics on Reddit:\n")
    for i, topic in enumerate(posts, 1):
        print(f"{i}. {topic}")

    print("\nAI-Generated Tweet Ideas:\n")
    for topic in posts:
          idea = generate_idea(topic)
          print(f"Topic: {topic}\nTweet Idea: {idea}\n")  

print(f"Topic: {topic}\nTweet Idea: {idea}\n{'-'*80}\n")

with open("output.txt", "w") as f:
    for topic in posts:
        idea = generate_idea(topic)
        f.write(f"Topic: {topic}\nTweet Idea: {idea}\n\n")
