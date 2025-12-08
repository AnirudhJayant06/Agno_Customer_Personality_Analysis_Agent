import sys
import os
import json
from agno.agent import Agent
from pathlib import Path

# from agno.models.openrouter import OpenRouter
# from agno_app.config import settings

from dotenv import load_dotenv
from agno.models.groq import Groq

# To load environment variables from env file
load_dotenv()

# This file: .../Agno_Customer_Personality_Analysis_Agent/agents/data_agent.py
THIS_FILE = Path(__file__).resolve()

# agents/ folder
AGENTS_DIR = THIS_FILE.parent

# Project root = parent of "agents"
PROJECT_ROOT = AGENTS_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def get_user_query():
    print("""
    ------------------------------
           What this Agent can do?
    ------------------------------
    1. Can Give You Global Statistics
    2. Can Give You Segment-Based Statistics based on
          - Marital Status: Married/ Single/ Together/ Divorced/ Widow
          - Has Children or Not
          - High-Value Customers or Not
    3. Can Give You Stats of Top 'n' Spending Customers
          
    (e.g., "Show top 5 high-value customers with kids")
          
    Note: Enter 'Q' to quit.
    
    """)

    while True:
        query = input("\nEnter your query: ").strip()

        # Quit condition
        if query.lower() == "q":
            print("\nExiting... Goodbye! 👋")
            return None  # or break, depending on your design

        # Handle empty input
        if not query:
            print("⚠️  Empty input — please write your query or enter 'Q' to quit.")
            continue
        
        # Return the query to the main agent loop
        return query
    

from tools.data_tools import (
    global_stats,
    segment_stats,
    top_customers_by_spend,
)

def get_tools_used(resp):
    return [t.tool_name for t in resp.tools]


def create_data_agent(model) -> Agent:
    """
    Create the Data Agent.

    - Use any model
    - Has access to 3 tools over the marketing dataset.
    - Is instructed to NEVER guess numbers, only use tools.
    """

    agent = Agent(
        name="Data Agent",

        # This defines the agent's behavior
        # Role = Who you are + what you do.
        role=(
            "You are a precise data analytics agent over the marketing_campaign dataset. "
            "You NEVER guess numeric values. "
            "You must always call the available tools (global_stats, segment_stats, "
            "top_customers_by_spend) to obtain statistics. "
            "Return your final answer as VALID JSON only, with numeric fields and short labels."
        ),
        model=model,
        tools=[
            global_stats,
            segment_stats,
            top_customers_by_spend,
        ],

        # These are additional instructions for the agent to perform better
        # Instructions = How you must behave while doing it.
        instructions=[
            "You MUST use the provided tools to inspect the REAL dataset instead of guessing"
            " (counts, averages, sums, percentages, etc.).",
            "You are FORBIDDEN from guessing or inventing numeric values.",
            "If a tool fails or is unavailable, say you cannot answer instead of guessing.",
            "When calling a tool with no parameters, always use {} as the arguments object.",
            "If the user explicitly asks for a raw list, table, JSON array, or 'do not summarize', "
            "then return the tool's JSON output directly (possibly lightly reformatted) without aggregation.",
            "If the user asks for 'summary', 'stats', 'insights', or similar, you may compute aggregate "
            " statistics over the tool output (e.g., averages, min, max) and return a summarized view.",
            "If it is unclear, prefer returning both: a 'summary' section and a 'customers' list in the JSON.",

            # Style rules
            "Respond in short, clear bullet points without markdown headings.",
            "Do not use Markdown headings like ### or bold formatting.",
            
        ],
    )

    return agent

if __name__ == "__main__":

    # Create Groq model
    api_key = os.getenv("GROQ_API_KEY")
    model_id = os.getenv("GROQ_MODEL_ID")

    model = Groq(
        api_key=api_key,
        id=model_id,
        temperature=0.1,)


    # Quick manual test
    agent = create_data_agent(model)

    while True:
        query = get_user_query()
        if query is None:
            break  # user quit
        
        # Send the user’s query to LLM / agents here
        response = agent.run(query, stream=False)
        print("\n Here are your required statistics:", response.content)

        if response.tools:
            print("\n✅ Tools were used in this run.\n")
        else:
            print("❌ No tools were used - answer likely hallucinated.")
            #raise RuntimeError("Agent did not use any tools. Rejecting answer.")
    
        print('Tools used by the agent: ', get_tools_used(response))    

    '''
    stream=False => Returns complete response at once.
    stream=True => Returns response in a stream of chunks (tokens)
    '''

    