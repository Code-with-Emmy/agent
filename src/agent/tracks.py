from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-5-turbo",
        messages=messages,
    )

    reply = response.choices[0].message.content
    print(f"Assistant: {reply}")

    messages.append({"role": "assistant", "content": reply})