# Simple Tool Combination Demo
# This shows how OpenAI can combine multiple tools to solve problems

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

print("🔧 Tool Demo: Code Interpreter")
print("=" * 60)

# Example 1: Simple calculation with web data
print("\n📊 Example 1: Current data + calculation")
response = client.responses.create(
    model="gpt-5-nano",
    tools=[
        {"type": "code_interpreter", "container": {"type": "auto"}}
    ],
    input="I have invested USD 1000 at the rate of 10% per anum simple interest for 10 years. What will be the total amount after 10 years?Give me visulaisation of bar graph as well.",
)

print("✅ Result:")
print(response.output_text)

# print("\n" + "="*60)

# # Example 2: Simple analysis
# print("\n📈 Example 2: Research + analysis")
# response2 = client.responses.create(
#     model="gpt-5-nano",
#     tools=[
#         {"type": "web_search"},
#         {"type": "code_interpreter", "container": {"type": "auto"}}
#     ],
#     input="Find Infosys's current stock price and calculate what a INR 100000 investment made 1 year ago would be worth today.Today is 16th Nov 2025,"
# )

# print("✅ Result:")
# print(response2.output_text)

# print("\n" + "="*60)
# print("🎯 Key Learning: OpenAI automatically chose which tools to use and in what order!")
# print("   • Web search for current data")
# print("   • Code interpreter for calculations") 
# print("   • All combined seamlessly!")