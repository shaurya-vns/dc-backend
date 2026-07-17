from groq import Groq
from django.conf import settings

client = Groq(
    api_key= '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'
)

response = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)