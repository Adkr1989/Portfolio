# ADEV Agent Orchestration Dashboard

**Status:** 🟢 Production | **Type:** Internal Tool | **Purpose:** Multi-Agent Management

## Overview

Real-time agent orchestration platform managing 6 specialized subagents for enterprise AI automation. Features secure WebSocket streaming, API key authentication, and HTTPS deployment with self-signed certificates.

## System Architecture

```
┌────────────────────────────────────────────────────────┐
│                  Web Dashboard                         │
│            (React + WebSocket Client)                  │
│                                                        │
│  - Real-time agent status                             │
│  - Task submission                                     │
│  - Streaming responses                                 │
│  - Usage analytics                                     │
└───────────────────────┬────────────────────────────────┘
                        │ HTTPS/TLS
                        │ API Key Auth
┌───────────────────────▼────────────────────────────────┐
│              FastAPI Backend                           │
│         (Python + Agent Orchestrator)                  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │         Agent Orchestrator                       │  │
│  │                                                  │  │
│  │  - Route tasks to subagents                     │  │
│  │  - Manage execution queue                       │  │
│  │  - Aggregate results                            │  │
│  │  - Stream updates via WebSocket                 │  │
│  └──────────┬──────────────────────────────────────┘  │
│             │                                          │
│  ┌──────────▼──────────────────────────────────────┐  │
│  │        6 Specialized Subagents                   │  │
│  │                                                  │  │
│  │  ┌────────────┐  ┌─────────────────┐           │  │
│  │  │  Grant     │  │  Compliance     │           │  │
│  │  │  Researcher│  │  Expert         │           │  │
│  │  └────────────┘  └─────────────────┘           │  │
│  │  ┌────────────┐  ┌─────────────────┐           │  │
│  │  │  Form      │  │  Agent          │           │  │
│  │  │  Filler    │  │  Developer      │           │  │
│  │  └────────────┘  └─────────────────┘           │  │
│  │  ┌────────────┐  ┌─────────────────┐           │  │
│  │  │  Workflow  │  │  Documentation  │           │  │
│  │  │  Builder   │  │  Writer         │           │  │
│  │  └────────────┘  └─────────────────┘           │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │       MCP Server Integration                     │  │
│  │                                                  │  │
│  │  - PowerShell Executor MCP                      │  │
│  │  - Playwright Browser MCP                       │  │
│  │  - Custom tool servers                          │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

## Technology Stack

- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Backend:** FastAPI (Python 3.11+)
- **AI Framework:** Claude Agent SDK (Anthropic)
- **Real-time:** WebSocket with asyncio
- **Security:** API Key Auth, HTTPS/TLS, self-signed certs
- **Protocol:** MCP (Model Context Protocol)

## Six Specialized Subagents

### 1. Grant Researcher
**Domain:** Federal and state grant programs

**Capabilities:**
- Search Grants.gov database
- Analyze eligibility requirements
- Calculate funding amounts
- Track application deadlines

**Example Use Case:**
> "Find NEVI formula grants for Illinois EV charging projects over $100K"

---

### 2. Compliance Expert
**Domain:** FDA/GMP/HACCP regulations

**Capabilities:**
- Verify regulatory compliance
- Check 21 CFR requirements
- Validate HACCP plans
- Search FDA recalls

**Example Use Case:**
> "Check if our facility meets FDA 21 CFR Part 117 for supplement manufacturing"

---

### 3. Form Filler
**Domain:** Automated document completion

**Capabilities:**
- Extract data from source documents
- Map fields to target forms
- Validate completeness
- Generate PDFs

**Example Use Case:**
> "Auto-fill FDA 510(k) application using our technical documentation"

---

### 4. Agent Developer
**Domain:** AI agent and tool development

**Capabilities:**
- Build Claude Agent SDK agents
- Create MCP servers
- Develop custom tools
- Write integration code

**Example Use Case:**
> "Create an MCP server for executing PowerShell compliance scripts"

---

### 5. Workflow Builder
**Domain:** n8n automation workflows

**Capabilities:**
- Design automation workflows
- Configure webhook integrations
- Set up Slack notifications
- Schedule recurring tasks

**Example Use Case:**
> "Build n8n workflow to sync Airtable grants to PostgreSQL database"

---

### 6. Documentation Writer
**Domain:** Technical documentation

**Capabilities:**
- Generate API documentation
- Write user guides
- Create architecture diagrams
- Produce README files

**Example Use Case:**
> "Write API documentation for the EV_LV platform endpoints"

---

## Core Features

### Real-Time WebSocket Streaming

```python
# Simplified streaming pattern
@app.websocket("/ws/agent")
async def agent_endpoint(websocket: WebSocket):
    await websocket.accept()

    async for message in websocket.iter_text():
        # Route to appropriate subagent
        agent = select_agent(message)

        # Stream response
        async for chunk in agent.execute_stream(message):
            await websocket.send_json({
                "type": "delta",
                "content": chunk
            })
```

### API Key Authentication

```python
# Security middleware
async def verify_api_key(x_api_key: str = Header(...)):
    stored_key = load_api_key()
    if x_api_key != stored_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key
```

### Agent Routing Logic

```python
# Intelligent task routing
class AgentRouter:
    def route(self, task: str) -> SubAgent:
        # Analyze task with Claude
        analysis = self.analyze_intent(task)

        # Select best agent
        if 'grant' in analysis.keywords:
            return self.agents['grant_researcher']
        elif 'compliance' in analysis.keywords:
            return self.agents['compliance_expert']
        # ... other routing logic

        return self.agents['default']
```

## Security Features

### HTTPS/TLS Encryption

```python
# Self-signed certificate setup
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    'certs/cert.pem',
    'certs/key.pem'
)

uvicorn.run(
    app,
    host="127.0.0.1",
    port=8765,
    ssl_certfile="certs/cert.pem",
    ssl_keyfile="certs/key.pem"
)
```

### API Key Management

```python
# Secure API key storage
def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

def save_api_key(key: str):
    # Store securely (not in source control)
    with open('.api_key', 'w') as f:
        f.write(key)
    os.chmod('.api_key', 0o600)  # Owner read/write only
```

## MCP Server Integration

### PowerShell Executor MCP

```python
# Custom MCP server for PowerShell execution
class PowerShellMCP:
    """Execute PowerShell scripts safely with sandboxing."""

    async def execute(self, script: str) -> Result:
        # Validate script
        if not self.is_safe(script):
            raise SecurityError("Script failed safety check")

        # Execute in sandbox
        result = await run_powershell(
            script,
            timeout=30,
            sandbox=True
        )

        return result
```

### Playwright Browser MCP

```python
# Browser automation via MCP
class PlaywrightMCP:
    """Automate browser interactions for web scraping."""

    async def navigate(self, url: str) -> Page:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            return page
```

## Performance Metrics

- **Response Time:** < 2 seconds (agent routing)
- **Streaming Latency:** < 100ms (first token)
- **Concurrent Connections:** 50+ WebSocket connections
- **Uptime:** 99.9% (local deployment)
- **Agent Accuracy:** 95%+ task routing success

## Development Workflow

### Claude Agent SDK Tutorial Progression

The platform includes 6 progressive examples:

1. **0_querying.py** - Basic Claude queries
2. **1_conversation.py** - Multi-turn conversations
3. **2_tools.py** - Tool integration
4. **3_streaming.py** - Streaming responses
5. **4_mcp.py** - MCP server usage
6. **5_subagents.py** - Multi-agent orchestration ⭐

### Running the Dashboard

```bash
# Install dependencies
uv sync

# Generate API key
python gui/agent_server.py --generate-key

# Start server
uv run python gui/agent_server.py --show-key

# Access dashboard
https://localhost:8765
```

## Dashboard Features

### Task Submission Interface

```javascript
// Frontend WebSocket client
const ws = new WebSocket('wss://localhost:8765/ws/agent');

ws.onopen = () => {
  ws.send(JSON.stringify({
    task: 'Find NEVI grants for Illinois',
    agent: 'grant_researcher'  // Optional routing
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'delta') {
    appendToOutput(data.content);
  } else if (data.type === 'complete') {
    showCompletion(data.usage);
  }
};
```

### Real-Time Status Monitoring

- Active agent status
- Task queue visualization
- Execution history
- Token usage analytics
- Error tracking

## Code Quality

- **Type Hints:** Full Python type annotations
- **Async/Await:** Modern async Python patterns
- **Error Handling:** Comprehensive exception handling
- **Logging:** Structured logging with context
- **Documentation:** Docstrings on all public methods

## Lessons Learned

### What Worked Well
✅ WebSocket provided excellent real-time UX
✅ Subagent pattern scaled well to 6 specialized agents
✅ MCP servers enabled powerful integrations
✅ API key auth was simple but effective
✅ FastAPI made development fast and enjoyable

### Challenges Overcome
🔧 Certificate trust issues → Clear user instructions
🔧 Agent routing accuracy → Added Claude-based intent analysis
🔧 Concurrent WebSocket management → Used ConnectionManager pattern
🔧 Streaming edge cases → Robust error handling

## Future Enhancements

- [ ] Add agent performance metrics
- [ ] Implement agent learning/feedback loop
- [ ] Build agent marketplace (shareable configs)
- [ ] Add multi-user support
- [ ] Create mobile app

## Related Code Samples

- [Multi-Agent Orchestration Pattern](../../code-samples/claude-agent-sdk/multi_agent_orchestration.py)
- [WebSocket Streaming Pattern](../../code-samples/fastapi-patterns/websocket_streaming.py)
- [MCP Integration Example](../../code-samples/claude-agent-sdk/mcp_integration.py)

## Related Projects

- [EV_LV Platform](../evlv-grant-platform/) - Uses grant_researcher subagent
- [Maine Scientific](../maine-scientific-compliance/) - Uses compliance_expert subagent

---

**Note:** This documentation demonstrates the architecture and orchestration patterns without exposing internal implementation details. The actual system includes proprietary agent configurations and business logic.
