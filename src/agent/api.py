from openai import OpenAI
import os
from dotenv import load_dotenv
from tracks import tracks

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant answering questions."},
        {"role": "user", "content": "Write a short poem about the ocean."},
        {"role": "assistant", "content": "The ocean's waves dance and play,\nReflecting the sun's golden ray.\nIts depths hold secrets untold,\nA world of wonder, brave and bold."},
    ],
)

print(response.choices[0].message.content)