# 🔧 OpenAI SDK - Cheat Sheet

## 📚 Key Concepts

### 1. **Basic API Connection**
```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # Uses OPENAI_API_KEY from .env
```

### 2. **Response Generation**
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Your prompt here",
    temperature=0.7  # 0=deterministic, 1=creative
)
print(response.output_text)
```

### 3. **Memory Management**
```python
# No Memory (Stateless)
response = client.responses.create(
    model="gpt-4o-mini",
    input="Hello"
)

# With Memory (Conversational)
conversation_history = []
conversation_history.append({"role": "user", "content": "Hello"})
response = client.responses.create(
    model="gpt-4o-mini",
    input=conversation_history
)
conversation_history.append({"role": "assistant", "content": response.output_text})
```

## 🔑 Important Files

| File | Purpose |
|------|---------|
| `Connecting_llm_one.py` | Basic API connection |
| `no_memory_chatbot_two.py` | Stateless chatbot |
| `memory_chatbot_three.py` | Conversational with history |
| `audio_four.py` | Text-to-speech (TTS) |
| `image_five.py` | Image generation (DALL-E) |
| `web_search_six.py` | Web search integration |
| `web_search_project_seven.py` | Advanced web search |
| `mcp_eight.py` | Model Context Protocol |
| `mcp_exercise_nine.py` | MCP exercises |
| `gpt_code_interpretor_ten.py` | Code execution |
| `code_image_eleven.py` | Code + image generation |
| `gpt_reasoning_12.py` | o1/o3 reasoning models |
| `gpt_reasoning_improved_13.py` | Advanced reasoning |

## 💡 Common Patterns

### 1. **Text Generation**
```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="Write a summary of...",
    temperature=0,
    max_output_tokens=500
)
```

### 2. **Image Generation (DALL-E)**
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A professional photo of a container ship",
    size="1024x1024",
    quality="standard",
    n=1
)
image_url = response.data[0].url
```

### 3. **Text-to-Speech**
```python
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
    input="Text to speak"
)
response.stream_to_file("output.mp3")
```

### 4. **Web Search Tool**
```python
response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input="Find latest info about..."
)
```

### 5. **Code Interpreter**
```python
response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    input="Analyze this data: [1,2,3,4,5]"
)
```

### 6. **MCP (Model Context Protocol)**
```python
response = client.responses.create(
    model="gpt-5-mini",
    tools=[{
        "type": "mcp",
        "server_label": "github",
        "server_url": "https://api.githubcopilot.com/mcp/",
        "headers": {"Authorization": f"Bearer {TOKEN}"}
    }],
    input="List my GitHub repos"
)
```

### 7. **Reasoning Models (o1/o3)**
```python
response = client.responses.create(
    model="o3-mini",  # or "o1-mini", "o1-preview"
    input="Solve this complex problem...",
    reasoning_effort="high"  # low, medium, high
)
```

## 🎯 Model Selection Guide

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `gpt-4o` | Complex tasks | Medium | $$ |
| `gpt-4o-mini` | Most tasks | Fast | $ |
| `o3-mini` | Reasoning | Slow | $$$ |
| `gpt-5-nano` | Simple tasks | Very Fast | $ |
| `dall-e-3` | Images | Medium | $$ |
| `tts-1` | Audio | Fast | $ |

## 📊 Parameters Guide

### Temperature
```python
temperature=0    # Deterministic, consistent
temperature=0.7  # Balanced (default)
temperature=1    # Creative, varied
```

### Max Tokens
```python
max_output_tokens=100   # Short response
max_output_tokens=500   # Medium
max_output_tokens=4000  # Long response
```

### Reasoning Effort (o1/o3 models)
```python
reasoning_effort="low"     # Quick thinking
reasoning_effort="medium"  # Balanced
reasoning_effort="high"    # Deep reasoning
```

## 🎓 Learning Path
1. ✅ Basic connection (`Connecting_llm_one.py`)
2. ✅ Stateless chat (`no_memory_chatbot_two.py`)
3. ✅ Memory management (`memory_chatbot_three.py`)
4. ✅ Multimodal (audio, images)
5. ✅ Tool usage (web_search, code_interpreter)
6. ✅ MCP integration
7. ✅ Reasoning models

## 🚀 Quick Start Template
```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def ask(prompt):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.7
    )
    return response.output_text

# Use it
answer = ask("What is AI?")
print(answer)
```

## 🔍 Debugging Tips
```python
# Print full response object
print(response)

# Check for errors
try:
    response = client.responses.create(...)
except Exception as e:
    print(f"Error: {e}")

# Monitor token usage
print(f"Tokens used: {response.usage.total_tokens}")
```

## 💰 Cost Optimization
- Use `gpt-4o-mini` for most tasks
- Set `max_output_tokens` limits
- Cache repeated prompts
- Use `temperature=0` for consistent outputs
