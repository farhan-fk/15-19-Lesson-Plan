from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

GITHUB_PAT = os.getenv("GITHUB_PAT")  # Set this in your .env file  


def farhan_code_audit():
    """
    Audit internal repositories for code quality and documentation
    Useful for: Engineering teams, DevOps, Tech leads
    """
    
    print("=" * 60)
    print("STEP 1: Scanning Farhan's repositories")
    print("=" * 60)
    
    # First LLM call - Get repository information via GitHub MCP
    repo_scan = client.responses.create(
        model="gpt-4o-mini",
        tools=[{
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://api.githubcopilot.com/mcp/",
            "headers": {"Authorization": f"Bearer {GITHUB_PAT}"},
            "require_approval": "never",
        }],
        input="""List repositories for 'farhan-fk'.
        For each repo, check:
        1. Does it have a README?
        2. Last commit date
        3. Number of open issues
        4. Primary programming language
        
        Format as a structured list.""",
        max_output_tokens=800,
    )
    
    repo_info = repo_scan.output_text
    print("\n📊 Repository Scan Results:")
    print(repo_info)
    
    print("\n" + "=" * 60)
    print("STEP 2: Generating improvement recommendations")
    print("=" * 60)
    
    # Second LLM call - Analyze and recommend improvements
    recommendations = client.responses.create(
        model="gpt-4o-mini",
        input=f"""Based on this repository scan of Farhan's internal tools:

{repo_info}

Generate an actionable report for the engineering manager:

1. **Critical Issues** - Repos that need immediate attention (no README, old commits, many issues)
2. **Documentation Gaps** - Which repos need better documentation
3. **Maintenance Priority** - Ranking of repos by urgency (1-10)
4. **Quick Wins** - Easy improvements we can do this week
5. **Action Items** - Specific tasks with owners

Format as a professional email.""",
        instructions="Be concise, actionable, and prioritize by business impact.",
        temperature=0.7,
        max_output_tokens=1000,
    )
    
    print("\n📋 Manager Report:")
    print(recommendations.output_text)
    
    return {
        "scan": repo_info,
        "recommendations": recommendations.output_text
    }


if __name__ == "__main__":
    farhan_code_audit()