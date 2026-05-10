from strands import Agent
from tools import mock_search, math_calculator

MODEL_ID = "us.amazon.nova-pro-v1:0"

# --- SWARM AGENTS ---

search_agent = Agent(
    name="search_agent",
    model=MODEL_ID,
    system_prompt="You find raw facts and data about the given topic. Keep it concise. Use your search tool to find accurate information.",
    tools=[mock_search]
)

fact_checker_agent = Agent(
    name="fact_checker_agent",
    model=MODEL_ID,
    system_prompt="You review the facts provided by the search agent and verify if they make logical sense. Highlight any discrepancies or confirm validity."
)

# --- GRAPH AGENTS ---

math_expert = Agent(
    name="math_expert",
    model=MODEL_ID,
    system_prompt="You are a math expert. Extract numerical data from the text and compute any necessary computations or statistics. Use your calculator tool when needed.",
    tools=[math_calculator]
)

analysis_agent = Agent(
    name="analysis_agent",
    model=MODEL_ID,
    system_prompt="You analyze the verified facts. If there are numbers to compute, you must use your math_expert tool.",
    tools=[math_expert]
)

report_agent = Agent(
    name="report_agent",
    model=MODEL_ID,
    system_prompt="You take the analyzed data and format it into a beautiful markdown report. Include a title, key statistics, bullet points, and a summary."
)
