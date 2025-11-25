from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

print("Chatbot started! Type 'quit' to exit.\n")

conversation_history = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye!")
        break
    
    conversation_history.append(f"user: {user_input}")
    
    messages_text = "\n".join(conversation_history)
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages_text,
        instructions="Be concise and helpful. Consider the full conversation history.",
    )
    
    conversation_history.append(f"assistant: {response.output_text}")
    
    print(f"Bot: {response.output_text}\n")