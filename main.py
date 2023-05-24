"""main.py - simple command line interface to OpenAI's API.

It's quite easy. Prereq:
1. Obtain an API key at https://platform.openai.com/account/api-keys
2. Set the OPENAI_API_KEY environment variable to the key value
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
q - quit
i prompt - create an image from a prompt
s prompt - create a simple response from a prompt
"""

def create_image(prompt : str, size : int = 256, num_images : int = 1) -> str:
    """Returns the url of an image generated by OpenAI from a text prompt."""
    response = openai.Image.create(
        prompt=prompt,
        n=num_images,
        size=f"{size}x{size}"
    )
    return response['data'][0]['url']

def display_image(url : str) -> None:
    """Displays an image from a url."""
    # Download the image with no SSL context, then display it using PIL
    with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as response:
        image_bytes = response.read()
    image = PIL.Image.open(io.BytesIO(image_bytes))
    image.show()

def create_simple_response (prompt : str) -> str:
    """returns the text response from OpenAI from a text prompt."""
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    """Main function"""
    print (HELP)
    while True:
        cmd = input("What do you want to do? ")
        if cmd[0] == 'q':
            break
        elif cmd[0] == 'h':
            print (HELP)
        elif cmd[0] == 'i':
            prompt = cmd[2:]
            img = create_image(prompt)
            display_image(img)
        elif cmd[0] == 's':
            prompt = cmd[2:]
            print (create_simple_response(prompt))
        else:
            print ("Unknown command.")
    print ("Goodbye!")

if __name__ == "__main__":
    main()
