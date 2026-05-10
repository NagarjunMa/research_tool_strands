from strands.multiagent import Swarm, GraphBuilder
from agents import search_agent, fact_checker_agent, analysis_agent, report_agent

def build_pipeline():
    """
    Builds the final capstone multi-agent graph pipeline.
    Combines:
      - Swarm (search_agent + fact_checker_agent)
      - Agent-as-a-tool (analysis_agent using math_expert internally)
      - Graph routing (Swarm -> Analysis -> Report)
    """
    
    # 1. Create the Swarm
    research_swarm = Swarm(
        nodes=[search_agent, fact_checker_agent],
        entry_point=search_agent,
        max_iterations=3
    )

    # 2. Build the Graph
    builder = GraphBuilder()

    # Add Nodes
    node_swarm = builder.add_node(research_swarm, node_id="research_swarm")
    node_analysis = builder.add_node(analysis_agent, node_id="analysis")
    node_report = builder.add_node(report_agent, node_id="report")

    # Add Edges
    builder.add_edge(node_swarm, node_analysis)
    builder.add_edge(node_analysis, node_report)

    # Set Entry Point
    builder.set_entry_point("research_swarm")

    # Build and return
    graph = builder.build()
    return graph
