from openai import OpenAI
from app.config import Config


# Create OpenRouter client
client = OpenAI(
    api_key=Config.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


print("\n========== OPENROUTER LLAMA TEST ==========")

try:

    response = client.chat.completions.create(
        model=Config.OPENROUTER_MODEL,

        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: OpenRouter Llama test successful"
            }
        ],

        temperature=0
    )

    print("Model:", Config.OPENROUTER_MODEL)
    print("Response:")
    print(response.choices[0].message.content)

    print("===========================================")

except Exception as error:

    print("OpenRouter request failed:")
    print(error)