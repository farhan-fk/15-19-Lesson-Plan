from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

os.makedirs("maersk_outputs", exist_ok=True)

print("🔧 Investment Calculator with gpt-4o")
print("=" * 60)

response = client.responses.create(
    model="gpt-4o",  # More reliable for code execution
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    input="""Calculate simple interest and create a bar chart:

Principal: $1000
Rate: 10% per annum
Time: 10 years

Write Python code to:
1. Calculate the values
2. Create a matplotlib bar chart
3. Save as PNG file
4. Return the file to me

Make sure to actually execute the code and provide the image file.""",
    max_output_tokens=2000,
)

print("\n✅ Response:")
print(response.output_text)

# Extract files
print("\n📁 Looking for files...")
files_found = False

if hasattr(response, 'output'):
    for idx, item in enumerate(response.output):
        item_data = item.model_dump() if hasattr(item, 'model_dump') else {}
        
        if item_data.get('type') == 'image':
            files_found = True
            file_id = item_data.get('image', {}).get('file_id')
            
            if file_id:
                print(f"✅ Found file_id: {file_id}")
                try:
                    content = client.files.content(file_id)
                    filepath = "maersk_outputs/investment_chart.png"
                    
                    with open(filepath, "wb") as f:
                        f.write(content.content)
                    
                    print(f"💾 Saved: {filepath}")
                    
                    # Auto-open
                    import platform
                    if platform.system() == 'Darwin':  # macOS
                        os.system(f'open "{filepath}"')
                    elif platform.system() == 'Windows':
                        os.system(f'start "" "{filepath}"')
                    else:  # Linux
                        os.system(f'xdg-open "{filepath}"')
                    
                except Exception as e:
                    print(f"❌ Error: {e}")

if not files_found:
    print("⚠️  No images found - saving debug info...")
    import json
    with open("maersk_outputs/debug.json", "w") as f:
        json.dump(response.model_dump(), f, indent=2, default=str)
    print("📄 Saved: maersk_outputs/debug.json")

print("\n" + "=" * 60)