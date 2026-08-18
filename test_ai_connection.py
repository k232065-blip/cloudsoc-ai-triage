from openai import OpenAI
import os

api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    print("ERROR: OPENROUTER_API_KEY not found in environment")
    exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {"role": "user", "content": "Say hello and confirm you are working, in one short sentence."}
    ]
)

print("API Response:")
print(response.choices[0].message.content)
