import streamlit as st
import json
import time
import requests
import os

# Optionally point this to your actual AWS Lambda Function URL once deployed!
# LAMBDA_URL = "https://your-function-url.aws/"
LAMBDA_URL = os.environ.get("LAMBDA_URL", "")

st.set_page_config(page_title="Topic Research Assistant", page_icon="🕵️", layout="centered")

st.title("🕵️ Multi-Agent Topic Research")
st.markdown("Powered by Strands SDK (Swarm + Graph + Agents-as-Tools)")

# Sidebar for config
with st.sidebar:
    st.header("Configuration")
    use_local = st.toggle("Run Locally (Simulator)", value=True, help="If toggled off, will make an HTTP request to the LAMBDA_URL")
    if not use_local:
        lambda_endpoint = st.text_input("Lambda URL", value=LAMBDA_URL)

topic = st.text_input("What topic would you like to research?", placeholder="e.g. Apollo 11 or Ocean Acidification")

if st.button("Generate Report", type="primary"):
    if not topic:
        st.warning("Please enter a topic to research.")
    else:
        with st.spinner("Agents are orchestrating... this may take up to 30 seconds."):
            start_time = time.time()
            
            payload = {"topic": topic}
            
            try:
                if use_local:
                    # Run it locally via direct import for demonstration
                    from handler import lambda_handler
                    mock_event = {"body": json.dumps(payload)}
                    response = lambda_handler(mock_event, {})
                    
                    if response.get("statusCode") == 200:
                        data = json.loads(response["body"])
                        report = data.get("report", "No report generated.")
                        st.success(f"Report generated in {time.time() - start_time:.1f} seconds!")
                        st.markdown("---")
                        st.markdown(report)
                    else:
                        st.error(f"Error: {response.get('body')}")
                else:
                    # Run it via HTTP request to AWS Lambda
                    if not lambda_endpoint:
                        st.error("Please provide a valid Lambda URL in the sidebar.")
                    else:
                        res = requests.post(lambda_endpoint, json=payload, timeout=60)
                        res.raise_for_status()
                        
                        data = res.json()
                        if data.get("status") == "success":
                            st.success(f"Report generated in {time.time() - start_time:.1f} seconds!")
                            st.markdown("---")
                            st.markdown(data.get("report", ""))
                        else:
                            st.error(f"Lambda Error: {data}")
                            
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
