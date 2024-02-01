from openai import OpenAI

client = OpenAI(api_key='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')

def getValues():
    c = open("responses.txt", "r")
    content = c.read()
    c.close()
    response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    response_format={ "type": "json_object" },
    messages=[
      { "role": "system", "content": 
          "You will be given 3 lines describing a situation, each line describes either mood, activity, or setting.\
            You are to output, from a scale from 0.0 - 1.0, how important is this trait is a song to fit the situation given. \
            0.0 would be not required, 1.0 would be required, and 0.5 would be indifferent\
            Answer in a JSON format, each on a new line: \
            Danceability\
            Energy\
            Instrumentalness\
            Liveness\
            Loudness\
            Tempo (ANSWER IN BPM (Min 30, Max 200)) \
            Valence"},
      { "role": "user", "content": content}
    ]
    )
    # print(response.choices[0])
    f = open("values.json", "w")
    f.write(response.choices[0].message.content)
    f.close()

