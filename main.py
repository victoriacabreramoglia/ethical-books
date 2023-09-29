import os
from dotenv import load_dotenv
import ipdb
import openai
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io
import base64
import textwrap

class ChildrenBookCreator:
    def __init__(self, entries, output_path):
        self.entries = entries
        self.output_path = output_path

    def create_book(self):
        page_width = 2048
        page_height = 1024
        pagesize = (page_width, page_height)

        # Create a canvas with the custom page size
        c = canvas.Canvas(self.output_path, pagesize=pagesize)
        
        for entry in self.entries:
            self._create_page(c, entry, page_width, page_height)
            c.showPage()  # End the current page and begin a new one
        
        c.save()

    def _create_page(self, c, entry, width, height):
        # Load the image
        image_data = base64.b64decode(entry['image'])
        image = Image.open(io.BytesIO(image_data))

        # The image is always 1024x1024, draw it at the start of the page
        image_width = 1024  # The actual width to draw the image
        image_height = height  # The designated height for the image
        
        x_position = 0  # Start at the beginning of the page
        y_position = 0
        
        # Draw the image
        c.drawInlineImage(image, x_position, y_position, width=image_width, height=image_width)  # Image is square
        
        # Calculate the text area dimensions
        text_width = 1024
        text_x_position = 1134  # Start text a little bit inside of the text area
        
        # Create a text object for the caption and set font and text
        text_object = c.beginText()
        text_object.setFont("Helvetica", 36)
        text_object.setTextOrigin(text_x_position, 800)  # Start text a little bit inside and from the top of the text area
        
        # Wrap the text within the available text width
        wrapper = textwrap.TextWrapper(width=40)  # Adjust the division factor to fit the text properly
        wrapped_text = wrapper.fill(entry['caption'])
        
        # Add the wrapped text to the text object
        text_object.textLines(wrapped_text)
        
        # Draw the text object with word wrapping within the text area
        c.drawText(text_object)







def call_gpt(messages_list):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_list,
        temperature=.8,
    )["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # initial setup
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
    openai.organization = OPENAI_ORG_ID
    openai.api_key = OPENAI_API_KEY
    # /initial setup

    # system: instructions for the machine. "how" you want it to respond. ex from documentation: "When I ask for help to write something, you will reply with a document that contains at least one joke or playful comment in every paragraph."
    # assistant: chaptgpt character. what we're telling chatgpt that chatgpt said. need to provide all context of conversation history in each call
    # user: user character. what we're telling chatgpt that the user said

    STORY_PROMPT = "A young samurai goes on a journey to prove himself."
    #STORY_PROMPT = "A little girl named Sabryna and her cat named Mr. Cat enjoy a day at the pumpkin patch."
    NUM_SCENES = 5 # 5 images/minute seems to be DALL-E limit until we look further into it
    story_outline = call_gpt(
        [
            {
                "role": "system",
                "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into a complete narrative arc. The story should be a complete story with one character. Include a CHARACTER section with the character's name and what they look like.",
            },
            {"role": "user", "content": STORY_PROMPT},
        ]
    )
    print(story_outline)
    story_beats = call_gpt(
        [
            {
                "role": "system",
                "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into " + str(NUM_SCENES) + " scenes that could be illustrated in a children's book. Each scene should be a sentence or two, and you should focus on describing the protagonist of the story and what they are doing in the scene.Start with the word scene, and separate each scene with the word scene. Each time, briefly describe each character in three or four words based on the story outline. Say what kind of creature they are. Always describe the character in the words in the character description from the narrative outline.",
            },
            {"role": "user", "content": story_outline},
        ]
    )
    story_beats = call_gpt(
        [
            {
                "role": "system",
                "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into " + str(NUM_SCENES) + " scenes that could be illustrated in a children's book. Each scene should be a sentence or two, and you should focus on describing the protagonist of the story and what they are doing in the scene.Start with the word scene, and separate each scene with the word scene. Each time, briefly describe each character in three or four words based on the story outline. Say what kind of creature they are. Always describe the character in the words in the character description from the narrative outline.",
            },
            {"role": "user", "content": story_outline},
            {"role": "system", "content": story_beats},
            {
                "role": "user",
                "content": "Okay, try that again, making sure that each scene has a creature, an explicit mention of the type of creature, and what it is doing. The description should be very action-oriented. Say NOUN does VERB in SOME PLACE. You can variate on that theme, but keep it close. Provide a lot of visual detail about the character and what they are doing.",
            },
        ]
    )
    story_beats = story_beats.split("Scene")[1:]
    story_beats_string = ""
    print("\nStory beats:")
    for beat in story_beats:
        print(beat)
        story_beats_string += beat + "\n"
    story_captions = call_gpt(
        [
            {
                "role": "system",
                "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a list of scene descriptions that make up the plot of the book. Please rewrite these descriptions in a happy, child-friendly, playful voice in simple vocabulary. Keep it expositional so we know what is happening in the scene. Include dialogue every once in a while. If the items in the list begin with numbers, remove them. If the items in the list begin with titles like ""Introduction"", remove them. This output is what is going to be shown to the reader and should include nothing but the scene descriptions separated only by a new line.",
            },
                {"role": "user", "content": "List of scene descriptions: " + story_beats_string}
        ]
    )
    print("\nstory_captions string: \n" + story_captions)
    story_captions = story_captions.split("\n\n")
    print("\nstory_captions string split into array:")
    for caption in story_captions:
        print(caption)
    # story_vibe = call_gpt(
    #     [
    #         {
    #             "role": "system",
    #             "content": "You are a professional children's book author creating material for a publishing house. You are going to receive a story concept. Turn it into short blurb that describes an aesthetic vocabulary for the art style of the book. It should be something like 'Digital art. Stylish. 1950s American art. Funny, upbeat.' Mix aesthetic language and emotional language to capture the vibe of the story. Keep it to five words.",
    #         },
    #         {"role": "user", "content": story_outline},
    #     ]
    # )
    story_vibe ="Anime. Cel-shaded. Digital ink. Japanese."
    prompts = []
    images_captions = []

    # Define a unique variable (using timestamp) for file output and create the output directory structure
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_directory = os.path.join("OUTPUT", timestamp, "RAW_PDFS")
    os.makedirs(output_directory, exist_ok=True)


    # go though each scene of the story. generate a user-facing caption and image
    for index, scene in enumerate(story_captions):
        print("\nloop iteration: " + str(index))
        print("\nscene: " + scene)

        image_resp = openai.Image.create(prompt=story_vibe + " " + scene, n=1, size="1024x1024", response_format = 'b64_json')
        image_string = image_resp['data'][0]['b64_json']

        # Decode the base64-encoded string and save it as an image file
        image_data = base64.b64decode(image_string)
        image_filename = os.path.join(output_directory, f"{index}.png")
        with open(image_filename, "wb") as image_file:
            image_file.write(image_data)
        
        images_captions.append(
            {
                "image":image_string,
                "caption": scene
            }
        )

    output_path = os.path.join(output_directory, f"{timestamp}.pdf")
    book_creator = ChildrenBookCreator(images_captions, output_path)
    book_creator.create_book()