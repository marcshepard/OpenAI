"""main.py - simple command line interface to OpenAI's API.

It's quite easy. Prereq:
1. Obtain an API key at https://platform.openai.com/account/api-keys
2. Either:
   2a. Set the OPENAI_API_KEY environment variable to the key value, or
   2b. Add a line of code to set the key value, e.g.:
           openai.api_key = "sk-xxxxxx"
       This is easier for testing, but don't check in to public repo or replit
3. Install the openai library, per https://platform.openai.com/docs/libraries.
4. Call some APIs. This script has API wrappers for chat and image generation:
    * https://platform.openai.com/docs/guides/chat/chat-vs-completions
    * https://platform.openai.com/docs/guides/images/introduction
But there are many other options.

It's quite inexpensive. See https://platform.openai.com/account/usage.
"""

import urllib.request
import io
import ssl
import PIL.Image
import openai   # pylint: disable=import-error

HELP = """
Available commands:
h - print this
c - chat
i - create an image
q - quit
"""

def create_image() -> str:
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
    with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as response:
        image_bytes = response.read()
    image = PIL.Image.open(io.BytesIO(image_bytes))
    image.show()


def create_chat () -> str:
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

def main():
    """Main function"""
    print (HELP)
    while True:
        cmd = input("What do you want to do? ").strip().lower()
        if cmd == 'h':
            print (HELP)
        elif cmd == 'i':
            create_image()
        elif cmd == 'c':
            create_chat()
        elif cmd == 'q':
            break
        else:
            print ("Unknown command. Type h for help.")
    print ("Goodbye!")

if __name__ == "__main__":
    main()
