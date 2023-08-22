"""main.py - simple command line interface to OpenAI's API.

It's quite easy. Prereq:
1. Obtain an API key at https://platform.openai.com/account/api-keys
2. Make the API key available to your code. There are several options:
   2a. PC Set the OPENAI_API_KEY environment variable to the key value, or
   2b. Replit: Under tools/secrets, add a key named OPENAI_API_KEY and set the value.
3. Install the openai library, per https://platform.openai.com/docs/libraries.
    * From personal PC with Python, run "pip install openai"
    * From Replit, it will automatically do this for you when you run the code
4. Call some APIs. This script has API wrappers for chat and image generation:
    * https://platform.openai.com/docs/guides/chat/chat-vs-completions
    * https://platform.openai.com/docs/guides/images/introduction
But there are many other options.

It's quite inexpensive. See https://platform.openai.com/account/usage.
"""

# pylint: disable=line-too-long

import os
import sys
import urllib.request
import io
import PIL.Image
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

HELP = """
Available commands:
c - chat
i - create an image
q - create a quiz
x - exit
"""

QUIZ_HELP = """
Let's create a ChatGPT-generated quiz for each student based on they essay they submitted
The quiz should not be graded, because ChatGPT is not perfect.
But a very low score indicated a likelyhood of copying-without-understanding
"""

def create_image():
    """Create an image from a text prompt"""
    prompt = input("What do you want to see? ")
    size = 256        # Image size can be 256, 512, or 1024
    num_images = 1    # Number of generated images can be 1, 2, or 3

    # Create an image URL from the prompt using the OpenAI API
    response = openai.Image.create(
        prompt=prompt,
        n=num_images,
        size=f"{size}x{size}"
    )
    url = response['data'][0]['url']

    # Display the image URL
    with urllib.request.urlopen(url) as response:
        image_bytes = response.read()
    image = PIL.Image.open(io.BytesIO(image_bytes))
    image.show()


def create_chat ():
    """Start a chat settion with OpenAI's chatbot"""
    prompt = input("What do you want to say? ")
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    reply = response['choices'][0]['message']['content']
    print (f"OpenAI: {reply}")

def create_quiz ():
    """Create a quiz"""
    print (QUIZ_HELP)
    num_questions = 0
    while num_questions <= 0 or num_questions > 10:
        try:
            num_questions = int(input("How many questions should the quiz contain (1-10)? "))
        except ValueError:
            num_questions = 0
    essay = input ("Paste the student essay? Type an empty line with END to end the essay input.\n")
    while True:
        next_line = input().strip()
        if next_line.upper() == "END":
            break
        essay += "\n" + next_line

    print ("Creating quiz, be patient...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create a multiple choice quiz with {num_questions} questions based on a student essay. The goal of the quiz is to make sure the student understood the essay they submitted, and didn't just copy it without understanding what they wrote."},
            {"role": "user", "content": f"Essay: {essay}"},
        ],
        temperature=0.2,
    )
    reply = response['choices'][0]['message']['content']
    print (f"{reply}")

def goodbye():
    """Quit the program"""
    print ("Goodbye!")
    sys.exit(0)

def main():
    """Main function"""
    command_map = {
        'i': create_image,
        'c': create_chat,
        'q': create_quiz,
        'x': goodbye
    }
    while True:
        cmd = input("What do you want to do? ").strip().lower()
        if cmd in command_map:
            command_map[cmd]()
        else:
            print (HELP)

if __name__ == "__main__":
    main()
