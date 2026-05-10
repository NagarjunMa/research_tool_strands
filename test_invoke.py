import json
from handler import lambda_handler

if __name__ == "__main__":
    # Mock AWS API Gateway event
    mock_event = {
        "body": json.dumps({
            "topic": "The history and cost of the Apollo 11 moon landing"
        })
    }
    
    mock_context = {}
    
    print("Invoking local Lambda Handler...")
    response = lambda_handler(mock_event, mock_context)
    
    print("\n--- LAMBDA RESPONSE ---")
    print(f"Status Code: {response.get('statusCode')}")
    
    body = response.get("body")
    if body:
        parsed_body = json.loads(body)
        print("\n[Parsed JSON Body]")
        print(json.dumps(parsed_body, indent=2))
        
        print("\n--- FINAL RENDERED REPORT ---")
        print(parsed_body.get("report", ""))
