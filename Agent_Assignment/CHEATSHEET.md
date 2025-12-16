# 🎯 Agent Assignment - Cheat Sheet

## 📚 Key Concepts

### 1. **AI Agents**
- Autonomous programs that use LLMs to make decisions and take actions
- Can use multiple tools to accomplish complex tasks
- Maintain context across interactions

### 2. **Tool Calling**
```python
# Three types of tools:
1. Custom Tools    → Functions you define (e.g., lookup_order)
2. Built-in Tools  → OpenAI features (e.g., file_search)
3. External APIs   → Third-party services
```

### 3. **Vector Stores (RAG)**
- Store documents as embeddings for semantic search
- Used with `file_search` tool for FAQ/knowledge base queries
```python
vector_store = client.beta.vector_stores.create(name="kb")
file = client.files.create(file=open("faq.txt"), purpose="assistants")
client.beta.vector_stores.files.create(vector_store_id=vs.id, file_id=f.id)
```

### 4. **Agent Observability**
- Track agent behavior: tool calls, reasoning, performance
- Log to JSONL for analysis
```python
observer.log_event(event_type, data)
```

### 5. **Assistant API Pattern**
```python
# 1. Create Assistant
assistant = client.beta.assistants.create(
    model="gpt-4o-mini",
    tools=[{...}]
)

# 2. Create Thread (conversation)
thread = client.beta.threads.create()

# 3. Add Message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Query here"
)

# 4. Run Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# 5. Handle Tool Calls
if run.status == "requires_action":
    # Execute required tools and submit outputs
    client.beta.threads.runs.submit_tool_outputs(...)
```

## 🔑 Important Files

| File | Purpose |
|------|---------|
| `customer_support_agent.py` | Main agent implementation |
| `agent_observability.py` | Logging and tracking system |
| `orders_data.csv` | Sample order database |
| `maersk_faq.txt` | Knowledge base for RAG |
| `agent_logs.jsonl` | Agent execution logs |

## 💡 Common Patterns

### Custom Tool Definition
```python
{
    "type": "function",
    "function": {
        "name": "lookup_order",
        "description": "Find order by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    }
}
```

### Handling Tool Calls
```python
if tool.function.name == "lookup_order":
    args = json.loads(tool.function.arguments)
    result = lookup_order(args["order_id"])
```

## 🎓 Learning Path
1. ✅ Understand Assistant API flow
2. ✅ Create custom tools
3. ✅ Implement file_search for RAG
4. ✅ Add observability logging
5. ✅ Handle multi-turn conversations
6. ✅ Add new tools (Assignment!)

## 🚀 Quick Start
```bash
python customer_support_agent.py
```

## 📊 Key Metrics to Track
- Tool call frequency
- Response times
- Tool success/failure rates
- Conversation turns
- User satisfaction patterns
