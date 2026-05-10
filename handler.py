import json
from pipeline import build_pipeline
import strands._async as async_runner

def lambda_handler(event, context):
    """
    AWS Lambda handler for the Topic Research Assistant.
    Expects event payload like: {"body": '{"topic": "Apollo 11"}'}
    """
    print("Received event:", json.dumps(event))
    
    try:
        # Extract the topic from the event
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
            
        topic = body.get("topic", "Ocean Acidification")
        
        # Build and run the pipeline
        print(f"Building pipeline for topic: {topic}")
        graph = build_pipeline()
        
        # Note: If running inside Lambda, standard synchronous execution is fine.
        result = graph(topic)
        
        # Extract the final report output
        # The report is the output of the last node (report_agent)
        report_text = ""
        node_result = result.results.get("report")
        if node_result:
            for agent_result in node_result.get_agent_results():
                content = agent_result.message.get("content", [])
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        report_text += block["text"] + "\n"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "topic": topic,
                "status": "success",
                "report": report_text.strip()
            })
        }

    except Exception as e:
        print(f"Error executing pipeline: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
