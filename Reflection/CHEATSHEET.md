# 🔄 Reflection & Evaluation - Cheat Sheet

## 📚 Key Concepts

### 1. **What is Reflection?**
Self-improvement loop where an AI agent:
1. Generates initial output
2. Critiques its own work
3. Revises based on critique
4. Repeats until quality threshold is met

```
Generate → Critique → Revise → Evaluate → (Repeat or Done)
```

### 2. **Why Reflection?**
- ✅ Improves output quality
- ✅ Catches errors and inconsistencies
- ✅ Self-correcting behavior
- ✅ Better reasoning
- ❌ Without: Single-pass outputs, no self-correction

### 3. **Reflection vs Regular Prompting**
```python
# Regular (Single-pass)
output = llm("Write a report")

# Reflection (Multi-pass)
draft = llm("Write a report")
critique = llm(f"Critique this report: {draft}")
improved = llm(f"Revise based on critique: {draft}\n{critique}")
```

## 💡 Reflection Patterns

### Pattern 1: Simple Reflection
```python
def reflect_once(task):
    # Step 1: Generate
    draft = llm(f"Generate: {task}")
    
    # Step 2: Critique
    critique = llm(f"""
    Critique this output:
    {draft}
    
    What can be improved?
    """)
    
    # Step 3: Revise
    final = llm(f"""
    Original: {draft}
    Critique: {critique}
    
    Create improved version:
    """)
    
    return final
```

### Pattern 2: Multi-Round Reflection
```python
def reflect_multiple(task, max_rounds=3):
    output = llm(f"Generate: {task}")
    
    for i in range(max_rounds):
        critique = llm(f"Critique: {output}")
        
        # Check if satisfied
        if "no improvements needed" in critique.lower():
            break
            
        output = llm(f"Revise based on: {critique}\nOutput: {output}")
    
    return output
```

### Pattern 3: Reflection with Criteria
```python
def reflect_with_criteria(task, criteria):
    draft = llm(f"Generate: {task}")
    
    critique = llm(f"""
    Evaluate this output against these criteria:
    {criteria}
    
    Output: {draft}
    
    Score each criterion (1-10) and explain issues:
    """)
    
    final = llm(f"""
    Original: {draft}
    Evaluation: {critique}
    
    Revise to address all issues:
    """)
    
    return final
```

### Pattern 4: Tree-of-Thoughts
```python
def tree_of_thoughts(problem):
    # Generate multiple approaches
    approaches = []
    for i in range(3):
        approach = llm(f"Generate approach #{i+1} for: {problem}")
        approaches.append(approach)
    
    # Evaluate each
    evaluations = []
    for approach in approaches:
        eval = llm(f"Evaluate this approach: {approach}")
        evaluations.append(eval)
    
    # Choose best
    best = llm(f"""
    Which approach is best?
    {list(zip(approaches, evaluations))}
    """)
    
    return best
```

## 🔑 Important Files

| File | Purpose |
|------|---------|
| `eval_reflection.ipynb` | Reflection examples and evaluation |
| `utils.py` | Helper functions for reflection |
| `products.db` | Sample database for exercises |

## 🎯 Evaluation Metrics

### 1. **Quality Scoring**
```python
def evaluate_quality(output, criteria):
    score = llm(f"""
    Rate this output on a scale of 1-10 for:
    - Accuracy
    - Completeness
    - Clarity
    - Relevance
    
    Output: {output}
    Criteria: {criteria}
    
    Return as JSON:
    {{
        "accuracy": 8,
        "completeness": 7,
        "clarity": 9,
        "relevance": 8,
        "overall": 8.0
    }}
    """)
    return score
```

### 2. **Improvement Tracking**
```python
def track_improvement(drafts):
    scores = []
    for i, draft in enumerate(drafts):
        score = evaluate_quality(draft, criteria)
        scores.append({"round": i, "score": score})
    return scores
```

### 3. **Error Detection**
```python
def detect_errors(output):
    errors = llm(f"""
    List all errors in this output:
    - Factual inaccuracies
    - Logical inconsistencies
    - Missing information
    - Formatting issues
    
    Output: {output}
    """)
    return errors
```

## 🛠️ Reflection Prompts

### Self-Critique Prompt
```python
critique_prompt = """
Review your previous response and identify:

1. Factual errors or inaccuracies
2. Logical inconsistencies
3. Missing critical information
4. Areas that could be clearer
5. Formatting or structure issues

Be honest and thorough in your self-assessment.
"""
```

### Revision Prompt
```python
revision_prompt = """
You previously created this output:
{draft}

You identified these issues:
{critique}

Create an improved version that addresses all identified issues.
Maintain what was good, fix what was wrong.
"""
```

### Evaluation Prompt
```python
evaluation_prompt = """
Evaluate this output against the requirements:

Requirements:
{requirements}

Output:
{output}

Provide:
1. Score (1-10) for each requirement
2. Specific examples of what's good
3. Specific examples of what needs improvement
4. Overall recommendation (approve/revise/reject)
"""
```

## 📊 Reflection Strategies

### Strategy 1: Role Switching
```python
# Different perspectives
generator_role = "You are a content writer"
critic_role = "You are a harsh editor"
revisor_role = "You are a experienced writer incorporating feedback"
```

### Strategy 2: Criteria-Based
```python
criteria = {
    "accuracy": "All facts must be correct",
    "completeness": "Must cover all required points",
    "clarity": "Must be easy to understand",
    "conciseness": "No unnecessary words"
}
```

### Strategy 3: Comparative
```python
# Compare against examples
prompt = f"""
Compare this output to the gold standard example:

Your output: {output}
Gold standard: {gold_standard}

What's missing or different?
"""
```

## 🚨 Common Pitfalls

### 1. Insufficient Critique
```python
# ❌ Too general
critique = "This is good"

# ✅ Specific
critique = "Paragraph 2 lacks supporting data. The conclusion jumps to assumptions."
```

### 2. Not Using Critique
```python
# ❌ Ignoring feedback
draft = "Original text"
critique = "Add more examples"
revised = "Original text"  # No change!

# ✅ Actually revising
revised = "Original text with three concrete examples: 1) ... 2) ... 3) ..."
```

### 3. Infinite Loops
```python
# ❌ No stopping condition
while True:
    critique = llm(...)
    output = llm(...)

# ✅ Limit rounds
for i in range(MAX_ROUNDS):
    if quality_score > THRESHOLD:
        break
```

## 🎓 Learning Path
1. ✅ Understand single-pass vs reflection
2. ✅ Implement simple reflection (1 round)
3. ✅ Add multiple rounds
4. ✅ Implement scoring/evaluation
5. ✅ Create criteria-based reflection
6. ✅ Build tree-of-thoughts system

## 🚀 Quick Start Template

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def generate(prompt):
    return client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    ).output_text

def reflect(task):
    # Generate
    print("Generating initial draft...")
    draft = generate(f"Task: {task}")
    
    # Critique
    print("Critiquing draft...")
    critique = generate(f"""
    Critique this output and identify issues:
    {draft}
    """)
    
    # Revise
    print("Revising based on critique...")
    final = generate(f"""
    Original: {draft}
    Issues: {critique}
    
    Create improved version:
    """)
    
    return {
        "draft": draft,
        "critique": critique,
        "final": final
    }

# Use it
result = reflect("Write a shipping policy summary")
print("Final:", result["final"])
```

## 💡 Advanced Techniques

### 1. Multi-Agent Reflection
```python
writer_agent = "You are a writer"
editor_agent = "You are an editor"
fact_checker_agent = "You are a fact checker"

draft = agent(writer_agent, task)
factual_review = agent(fact_checker_agent, draft)
editorial_review = agent(editor_agent, draft)
final = agent(writer_agent, f"Revise based on: {factual_review}, {editorial_review}")
```

### 2. Reflection with Tools
```python
# Agent can use tools to verify claims
draft = generate(task)
critique = generate(f"Critique and identify claims to verify: {draft}")
verified_facts = search_tool(extract_claims(critique))
final = generate(f"Revise using verified facts: {verified_facts}")
```

### 3. Iterative Refinement with Scoring
```python
output = generate(task)
threshold = 8.0

for round in range(5):
    score = evaluate(output)
    if score >= threshold:
        break
    
    feedback = f"Current score: {score}. Needs improvement in: {get_weak_areas(score)}"
    output = generate(f"Improve: {output}\nFeedback: {feedback}")
```

## 🔍 Debugging Reflection
```python
# Log each step
def reflect_debug(task):
    print(f"Task: {task}")
    
    draft = generate(task)
    print(f"\n--- DRAFT ---\n{draft}\n")
    
    critique = generate(f"Critique: {draft}")
    print(f"\n--- CRITIQUE ---\n{critique}\n")
    
    final = generate(f"Revise: {draft}\nBased on: {critique}")
    print(f"\n--- FINAL ---\n{final}\n")
    
    return final
```

## 💰 Cost Considerations
- Each reflection round = 2-3 LLM calls
- 3 rounds = 6-9 LLM calls vs 1 call without reflection
- Use cheaper models for critique: `gpt-4o-mini`
- Save costs: Reflect only on important outputs

## 📈 Measuring Success
```python
# Compare with/without reflection
baseline = generate(task)
reflected = reflect(task)

# Evaluate both
baseline_score = evaluate(baseline)
reflected_score = evaluate(reflected)

improvement = reflected_score - baseline_score
print(f"Improvement: {improvement}")
```
