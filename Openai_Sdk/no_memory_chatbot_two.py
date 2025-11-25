from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

print("Chatbot started! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye!")
        break
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_input,
        instructions="Be concise and helpful.",
    )
    
    print(f"Bot: {response.output_text}\n")