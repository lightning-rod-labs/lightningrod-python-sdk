from openai import OpenAI

client = OpenAI(
    api_key="sk_8fca5e0f3d2e2c9e64a1f61f9bb24960447ab55f4e08edff3e724ad09084a3a7",
    base_url="https://api.lightningrod.ai/v1/openai",
)

response = client.chat.completions.create(
    model="foresight-v4",
    messages=[
        {"role": "user", "content": "Will Elon Musk still be the richest person by 2030?"},
    ],
)

print(response.choices[0].message.content)