from openai import OpenAI
from config import AI_TOKEN


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)

completion = client.chat.completions.create(
  model="deepseek/deepseek-chat",
  messages=[
    {
      "role": "user",
      "content": "Who is Hans Zimmer?"
    }
  ]
)
print(completion.choices[0].message.content)