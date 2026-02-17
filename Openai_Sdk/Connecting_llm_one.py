from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


# response = client.responses.create(
#     model="gpt-4o-mini",
#     input="Tell me Maersk's inception story in 100 words.",
#     instructions="Respond in a funny way, and include a joke about shipping.",
#     temperature=1,
#     max_output_tokens=200,
    
# )

# print("Response from LLM with tool integration:", response.output_text)


response = client.responses.create(
    model="gpt-4o-mini",
    input="63254*76729",
    instructions="Be concise and factual.",
    tools=[
        {"type": "code_interpreter", "container": {"type": "auto"}}
    ],
   
    
)

print("Response from LLM with tool integration:", response.output_text)

