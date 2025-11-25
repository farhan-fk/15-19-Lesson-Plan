from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----- Build prompt (same as yours) -----
today = datetime.now().date()
today_str = today.strftime("%Y-%m-%d")
departure_deadline = (datetime.now() + timedelta(hours=36)).strftime("%Y-%m-%d %H:00")

prompt = f"""
You are a senior global shipping planner for a major container line.

**Current Date:** {today_str}
**Departure Deadline:** {departure_deadline} (36 hours from now)

**Shipment Details:**
- Origin: Nhava Sheva (JNPT), Mumbai, India
- Destination: Rotterdam, Netherlands
- Containers: 250 TEU (each valued at $50,000)
- Total Cargo Value: $12.5 million
- Departure Window: MUST depart within 36 hours

**Priority Search Topics:**
1. Mumbai/JNPT port operational status (November 2025)
2. Red Sea/Suez Canal security situation (November 2025)
3. Rotterdam port disruptions (November 2025)

Provide routing recommendations with current disruption analysis.
"""

# ----- Call API -----
response = client.responses.create(
    model="gpt-5-nano",
    reasoning={"effort": "medium"},
    tools=[{"type": "web_search_preview"}],
    input=[{"role": "user", "content": prompt}]
)

# ----- Extract web search queries properly -----
print("="*70)
print("WEB SEARCH QUERIES MADE BY AI")
print("="*70)

search_count = 0
for idx, item in enumerate(response.output):
    # Convert to dict to inspect structure
    item_dict = item.model_dump() if hasattr(item, 'model_dump') else {}
    
    # Check if this is a web search item
    if item.type == "web_search" or "web_search" in str(item.type).lower():
        search_count += 1
        print(f"\n🔍 Search #{search_count}:")
        
        # Extract query from the dict structure
        if 'web_search' in item_dict:
            web_search_data = item_dict['web_search']
            if isinstance(web_search_data, dict):
                query = web_search_data.get('query') or web_search_data.get('search_query')
                print(f"   Query: {query}")
        elif 'query' in item_dict:
            print(f"   Query: {item_dict['query']}")
        elif 'search_query' in item_dict:
            print(f"   Query: {item_dict['search_query']}")
        else:
            print(f"   Query structure: {item_dict}")
        
        print(f"   Status: {item.status}")

if search_count == 0:
    print("\n⚠️ No web searches were performed")

# ----- Print final answer -----
print("\n" + "="*70)
print("SHIPPING ROUTE ANALYSIS")
print("="*70)
print(f"\nDate: {today_str}")
print(f"Departure Deadline: {departure_deadline}\n")
print(response.output_text)

# ----- Optional: Save to file -----
output_file = f"maersk_shipping_analysis_{today_str.replace('-', '')}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Maersk Shipping Route Analysis\n")
    f.write(f"Date: {today_str}\n")
    f.write(f"Departure Deadline: {departure_deadline}\n")
    f.write("="*70 + "\n\n")
    f.write(response.output_text)

print(f"\n💾 Analysis saved to: {output_file}")