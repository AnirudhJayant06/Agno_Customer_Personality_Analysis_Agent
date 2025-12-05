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

from tools.data_tools import (
    global_stats,
    segment_stats,
    top_customer_by_spend,
)

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
            top_customer_by_spend,
        ],

        # These are additional instructions for the agent to perform better
        # Instructions = How you must behave while doing it.
        instructions=[
            "You MUST use the provided tools to inspect the REAL dataset instead of guessing"
            " (counts, averages, sums, percentages, etc.).",
            "You are FORBIDDEN from guessing or inventing numeric values.",
            "If a tool fails or is unavailable, say you cannot answer instead of guessing.",
            "When calling a tool with no parameters, always use {} as the arguments object.",
            
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

    print("=== Test 1: Global stats ===")

    '''
    stream=False => Returns complete response at once.
    stream=True => Returns response in a stream of chunks (tokens)
    '''
    resp1 = agent.run(
        "Return overall stats for all customers as JSON.", stream=False)
    #print(dir(resp1))

    if resp1.tools:
        print("\n✅ Tools were used in this run.\n")
    else:
        print("❌ No tools were used – answer likely hallucinated.")
        #raise RuntimeError("Agent did not use any tools. Rejecting answer.")

    print("\n--- Agent Output ---\n")
    print(resp1.content)

    # To view the tool calls made by the agent during this run
    # print("\n=== RAW TOOLS ===\n")
    # for t in resp1.tools:
    #     if hasattr(t, "to_dict"):
    #         print("--- Tool as dictionary object ---")
    #         print(t.to_dict())
    #     else:
    #         print("--- Printing tool object as it is ---")
    #         print(t)

    # To view the complete json 
    # print('\n===To View the complete response as JSON:===\n')
    # '''
    # It is similar to resp1.to_json() but here we can format it better.
    # First, 'resp1' is converted to dict using to_dict() method.
    # Then, json.dumps() is used to convert the dict to a JSON string with indentation for readability.
    # - dumps() accepts other formats too like lists, tuples etc and converts them to JSON string.
    # - indent=2 is used for better readability.
    # - default=str is used to handle non-serializable objects by converting them to strings.
    # '''
    # # prints the JSON string (dump() is used to convert to JSON string)
    # print(json.dumps(resp1.to_dict(), 
    #                     indent=2, 
    #                     default=str))

    

    print("\n=== Test 2: Married, high-value customers with children ===")
    resp2 = agent.run(
        "Get stats (as JSON) for married customers who have children and are high-value.",
        stream=False,
    )
    print(resp2.content)

    print("\n=== Checking if any tools were used ===")
    if not resp1.tools:
        raise RuntimeError("Agent did not use any tools. Rejecting answer.")
    else:
        print(f"Agent used {len(resp1.tools) + len(resp2.tools)} tool(s).")