from strands import tool, Agent
from strands_tools import http_request, calculator
import time

@tool
def mock_search(query: str) -> str:
    """Search a database or the internet for facts about a given query."""
    try:
        time.sleep(0.5) # Simulate network delay
    
        query_lower = query.lower()
    
        agent = Agent(
            name="search",
            system_prompt="You are avid search expert. You will perform deep search on the topic requested by the user in the query",
            tools=[http_request]
        )

        result = agent(query_lower)
        return result
    except Exception as e:
        print(f"unable to complete the search : {e}")

@tool
def math_calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Only use this for basic arithmetic."""
    try:
        math_agent = Agent(
            name="math_agent",
            system_prompt="You are an expert in calculations and mathematics. Use the tool calculator whenever you need to compute mathematical expressions",
            tools=[calculator]
        )

        result = math_agent(expression)
        return result
    except Exception as e:
        return f"Error computing {expression}: {e}"
