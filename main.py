import os
from dotenv import load_dotenv
import ipdb
import openai

def call_gpt(messages_list):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages_list,
        temperature=.8
    )["choices"][0]["message"]["content"]

if __name__ == "__main__":
    # initial setup
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
    openai.organization = OPENAI_ORG_ID
    openai.api_key = OPENAI_API_KEY
    # /initial setup

    STORY_PROMPT = "Richard Nixon learns about love."
    story_outline = call_gpt(
        [
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into a complete narrative arc. The story should be a complete story with up to 3 characters."},
            {"role": "user", "content": STORY_PROMPT}
        ]
    )
    print(story_outline)
    story_beats = call_gpt(
        [
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into twelve scenes that could be illustrated in a children's book. Each scene should be a sentence or two, and you should focus on describing the protagonist of the story and what they are doing in the scene.Start with the word scene, and separate each scene with the word scene. Each time, briefly describe each character in three or four words based on the story outline. Say what kind of creature they are."},
            {"role": "user", "content": story_outline}
        ]
    )
    story_beats = call_gpt(
        [
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into twelve scenes that could be illustrated in a children's book. Each scene should be a sentence or two, and you should focus on describing the protagonist of the story and what they are doing in the scene.Start with the word scene, and separate each scene with the word scene. Each time, briefly describe each character in three or four words based on the story outline. Say what kind of creature they are."},
            {"role": "user", "content": story_outline},
            {"role": "system", "content": story_beats},
            {"role": "user", "content": "Okay, try that again, making sure that each scene has a creature, an explicit mention of the type of creature, and what it is doing. The description should be very action-oriented. Say NOUN does VERB in SOME PLACE. You can variate on that theme, but keep it close."}
        ]
    )
    story_vibe = call_gpt(
        [
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into short blurb that describes an aesthetic vocabulary for the art style of the book. It should be something like 'Digital art. Stylish. 1950s American art. Funny, upbeat.' Mix aesthetic language and emotional language to capture the vibe of the story. Keep it short."},
            {"role": "user", "content": story_outline}
        ]
    )
    story_beats = story_beats.split("Scene")[1:]
    for beat in story_beats:
        print(beat)
    prompts = []
    urls = []
    for beat in story_beats:
        image_resp = openai.Image.create(prompt=story_vibe + beat, n=1, size="1024x1024")
        caption = call_gpt(
        [
            {"role": "system", "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story outline, a specific scene, and a description of what's going on in that scene. Write the text that would go in a children's book alongside the image. Keep it to a about 4 sentences. Do not include anything except your one or two sentences. One sentence should be expository, telling us what is happening in the narrative. Remind us the overall narrative of the story pretty explicitly."},
            {"role": "user", "content": "Outline: " + story_outline + "Beat: " + beat}
        ]
    )
        url = image_resp['data'][0]['url']
        urls.append(
            {
                "url":url,
                "caption": caption
            }
        )
    ipdb.set_trace()