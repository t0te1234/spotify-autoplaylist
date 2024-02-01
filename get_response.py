from openai import OpenAI
from import_image import uploadImage

client = OpenAI(api_key='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')

def storeGPT(name):
  url = uploadImage(name)

  response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "The following image were all taken by a user going about their day. \
                                    Describe the mood, activity, and setting of the image. \
                                    Answer in this format, each on a new line: \
                                    Mood: <response> \
                                    Activity: <response> \
                                    Setting: <response>"},
          {
            "type": "image_url",
            "image_url": {
              "url": url,
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )
  f = open("responses.txt", "w")
  f.write(response.choices[0].message.content)
  f.close()
