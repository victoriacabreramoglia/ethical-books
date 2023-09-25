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
        temperature=2
    )["choices"][0]["message"]["content"]
    print(story_outline)
    story_beats = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into twelve scenes that could be illustrated in a children's book. Think about it like a storyboard artist. "},
            {"role": "user", "content": story_outline}
        ],
        temperature=2, 
        tokens=2000
    )["choices"][0]["message"]["content"]
    print(story_beats)