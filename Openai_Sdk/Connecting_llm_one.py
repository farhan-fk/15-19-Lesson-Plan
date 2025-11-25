from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


response = client.responses.create(
    model="gpt-4o-mini",
    input="Tell me Maersk's inception story in 200 words.",
    instructions="Be concise and factual.",
    temperature=1,
    max_output_tokens=200,
    
)

print("Response from LLM with tool integration:", response.output_text)