# 🕵️ Multi-Agent Topic Research Assistant

A serverless, multi-agent research pipeline built with the **Strands Agents SDK**. Given any topic, a swarm of specialized agents searches, fact-checks, analyzes, and renders a polished Markdown report — orchestrated as a directed graph and exposed via AWS Lambda + a Streamlit UI.

---

## ✨ Highlights

- **Multi-pattern orchestration** — combines three Strands primitives in one pipeline:
  - `Swarm` (collaborative search + fact-checking)
  - `Agent-as-a-tool` (analysis agent embeds a math expert)
  - `GraphBuilder` (deterministic routing between stages)
- **Amazon Bedrock Nova Pro** (`us.amazon.nova-pro-v1:0`) as the underlying LLM.
- **AWS Lambda deployable** with a public Function URL (no API Gateway required).
- **Streamlit front-end** with a local-simulator toggle, so you can demo without deploying.
- **One-command workflow** via `Makefile` (`install`, `test`, `ui`, `package`, `deploy`, `clean`).

---

## 🏗️ Architecture

```
                ┌─────────────────────────────────────────────┐
                │              GraphBuilder Pipeline           │
                │                                              │
   topic ──►    │   ┌──────────────────────┐                   │
                │   │   research_swarm     │                   │
                │   │  ┌────────────────┐  │                   │
                │   │  │ search_agent   │◄─┼── mock_search()   │
                │   │  │  ⇅ handoff     │  │     (http_request)│
                │   │  │ fact_checker   │  │                   │
                │   │  └────────────────┘  │                   │
                │   └──────────┬───────────┘                   │
                │              ▼                               │
                │   ┌──────────────────────┐                   │
                │   │   analysis_agent     │── tool ─► math_expert
                │   │                      │            (calculator)
                │   └──────────┬───────────┘                   │
                │              ▼                               │
                │   ┌──────────────────────┐                   │
                │   │    report_agent      │──► Markdown report
                │   └──────────────────────┘                   │
                └─────────────────────────────────────────────┘
```

### Stage breakdown

| Stage | Type | Agents | Responsibility |
|------|------|--------|----------------|
| 1. Research Swarm | `Swarm` (max 3 iters) | `search_agent`, `fact_checker_agent` | Gather raw facts and verify them collaboratively |
| 2. Analysis | Agent + nested agent-as-tool | `analysis_agent` → `math_expert` | Interpret verified facts, compute stats |
| 3. Reporting | Single agent | `report_agent` | Render a clean Markdown report |

---

## 📁 Project Structure

```
final_project/
├── agents.py          # Agent definitions (search, fact-checker, math, analysis, report)
├── tools.py           # Custom @tool wrappers: mock_search, math_calculator
├── pipeline.py        # Builds Swarm + Graph orchestration
├── handler.py         # AWS Lambda entry point (lambda_handler)
├── app.py             # Streamlit UI (local simulator or Lambda HTTP call)
├── test_invoke.py     # Local smoke test for the Lambda handler
├── requirements.txt   # Python deps
├── Makefile           # install / test / ui / package / deploy / clean
└── README.md
```

---

## 🤖 Agents

Defined in [`agents.py`](agents.py). All use Bedrock Nova Pro.

| Agent | Tools | Role |
|-------|-------|------|
| `search_agent` | `mock_search` | Finds raw facts about the topic |
| `fact_checker_agent` | — | Validates logical consistency, flags discrepancies |
| `math_expert` | `math_calculator` | Performs arithmetic/statistics |
| `analysis_agent` | `math_expert` (as tool) | Interprets verified data, delegates math |
| `report_agent` | — | Produces final Markdown report |

### Custom tools ([`tools.py`](tools.py))

- **`mock_search(query)`** — spins up a nested search agent equipped with `strands_tools.http_request` to perform deep web lookups.
- **`math_calculator(expression)`** — spins up a nested math agent equipped with `strands_tools.calculator` for safe arithmetic evaluation.

---

## 🚀 Quick Start

### 1. Prerequisites

- Python **3.12+**
- AWS credentials configured (`aws configure`) with **Bedrock Nova Pro access** in your region
- For deployment: an IAM role ARN with Lambda execution + Bedrock invoke permissions

### 2. Install

```bash
make install
# or:
pip install -r requirements.txt
```

### 3. Run locally (no AWS deploy needed)

**CLI smoke test:**
```bash
make test
# runs test_invoke.py against the Apollo 11 sample topic
```

**Streamlit UI:**
```bash
make ui
# opens http://localhost:8501
# keep "Run Locally (Simulator)" toggled ON in the sidebar
```

### 4. Deploy to AWS Lambda

```bash
export LAMBDA_ROLE_ARN=arn:aws:iam::<account-id>:role/<your-role>
make deploy
```

What it does:
- Packages source + deps into `deployment.zip`
- Creates `TopicResearchAssistant` Lambda (Python 3.12, 90s timeout) if missing, else updates code
- On first create: attaches a **public Function URL** (`auth-type NONE`) so the Streamlit app can hit it

Grab the Function URL from the AWS Console output, then in the Streamlit UI:
- Toggle **Run Locally** *off*
- Paste the URL into the sidebar
- Submit a topic

---

## 🔌 Lambda Invocation Contract

**Request** (Function URL POST body):
```json
{ "topic": "Apollo 11 moon landing" }
```

**Response**:
```json
{
  "topic": "Apollo 11 moon landing",
  "status": "success",
  "report": "# Apollo 11\n\n**Key Stats:** ...\n\n- bullet 1\n- bullet 2\n\n## Summary\n..."
}
```

Errors return `statusCode: 500` with a JSON `error` field.

---

## 🧪 Example Topics

- `Apollo 11 moon landing`
- `Ocean acidification`
- `Quantum supremacy milestones`
- `History of the transistor`

---

## 🛠️ Makefile Targets

| Target | Action |
|--------|--------|
| `make install` | Install Python deps |
| `make test` | Run `test_invoke.py` locally |
| `make ui` | Launch Streamlit app |
| `make package` | Build `deployment.zip` for Lambda |
| `make deploy` | Package + create/update Lambda function |
| `make clean` | Remove build artifacts |

---

## 🧰 Tech Stack

- **[Strands Agents SDK](https://strandsagents.com/)** — agents, swarms, graphs, tools
- **`strands-agents-tools`** — `http_request`, `calculator`
- **Amazon Bedrock** — Nova Pro foundation model
- **AWS Lambda** — serverless runtime with Function URLs
- **Streamlit** — front-end UI
- **Python 3.12**

---

## ⚙️ Configuration

| Variable | Purpose | Where |
|----------|---------|-------|
| `LAMBDA_URL` | Lambda Function URL for the Streamlit UI | env var or sidebar input |
| `LAMBDA_ROLE_ARN` | IAM role ARN used by `make deploy` | shell env |
| `MODEL_ID` | Bedrock model id (currently `us.amazon.nova-pro-v1:0`) | hardcoded in `agents.py` |

---

## 🧭 How the Pipeline Executes

1. `handler.lambda_handler` parses the incoming event, extracts `topic`.
2. `pipeline.build_pipeline()` constructs the `Swarm` and wires it into the `GraphBuilder` with two downstream edges (`research_swarm → analysis → report`).
3. The graph is invoked with the topic as input.
4. The `report` node's last `AgentResult.message.content` blocks are concatenated into the final Markdown string.
5. The handler returns `{ statusCode: 200, body: { report, ... } }`.

---

## 🧹 Cleanup

```bash
make clean
aws lambda delete-function --function-name TopicResearchAssistant
```

---

## 📜 License

MIT — use it, fork it, ship it.
