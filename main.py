import os
from dotenv import load_dotenv
import ipdb
import openai

if __name__ == "__main__":

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
    openai.organization = OPENAI_ORG_ID
    openai.api_key = OPENAI_API_KEY
    STORY_PROMPT = "An octopus and a shark go on a long journey together"
    story_outline = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into a complete narrative arc, and produce a precis for that narrative arc which is somewhat like a story board. The story should be a complete story with up to 3 characters."},
            {"role": "user", "content": STORY_PROMPT}
        ],
        temperature=.8
    )["choices"][0]["message"]["content"]
    print(story_outline)
    story_beats = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into twelve scenes that could be illustrated in a children's book. Think about it like a storyboard artist. Write a paragraph for each. Don't skimp! Separate scenes only with word scene. Start the response with the word scene."},
            {"role": "user", "content": story_outline}
        ],
        temperature=.8, 
        max_tokens=4000
    )["choices"][0]["message"]["content"]
    story_beats = story_beats.split("Scene")[1:]
    urls = []
    for beat in story_beats[0:2]:
        image_resp = openai.Image.create(prompt="Soft, cartoon, illustrated. Children's book style." + beat, n=4, size="1024x1024")
        url = image_resp['data'][0]['url']
        urls.append(url)
    ipdb.set_trace()