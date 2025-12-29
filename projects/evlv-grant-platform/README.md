# EV_LV Grant Intelligence Platform

**Status:** 🟢 Production | **Revenue:** $500/month | **Client:** Law Ventures LTD

## Overview

Production AI system for EV charging grant research serving energy consultants. Features AVA conversational agent with 12 specialized tools covering grant eligibility, NEVI compliance verification, and automated funding calculations.

## Business Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Grant Research Time | 40 hours | 15 minutes | **160x faster** |
| Programs Identified | 3-5 per search | 20+ per search | **4-6x more** |
| Accuracy | Manual review | 95%+ AI validation | **Consistent quality** |
| Client ROI | N/A | 10x cost savings | **$500/mo recurring** |

## Technology Stack

```
┌─────────────────────────────────────────────┐
│              Frontend Layer                 │
│           (WebSocket Client)                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          AVA Agent Core                     │
│      Claude API + Orchestration             │
│                                             │
│  - Natural language understanding           │
│  - Tool selection & routing                 │
│  - Context management                       │
│  - Response synthesis                       │
└──────┬─────────────────────────────┬────────┘
       │                             │
┌──────▼─────────┐          ┌────────▼────────┐
│  Tool Manager  │          │  Context Store  │
│                │          │                 │
│ 12 Specialized │          │ - User prefs    │
│ Tools:         │          │ - History       │
│ - Eligibility  │          │ - State         │
│ - Compliance   │          │ - Sessions      │
│ - Calculator   │          └─────────────────┘
│ - Analysis     │
│ - Search       │
│ - Validation   │
│ - etc.         │
└────────┬───────┘
         │
┌────────▼──────────────────────────────────────┐
│      External API Integrations                │
│                                               │
│  NREL    Grants.gov    ComEd    ChargeHub    │
└───────────────────────────────────────────────┘
```

## Core Technologies

- **AI Framework:** Claude API (Anthropic)
- **Backend:** Node.js, TypeScript, Express
- **Database:** PostgreSQL (Supabase)
- **Real-time:** WebSocket for streaming responses
- **Deployment:** Railway (auto-scaling, health monitoring)
- **Automation:** n8n Cloud (daily updates, notifications)
- **Integration:** 7+ external APIs

## Key Features

### 1. Conversational Interface (AVA)
- Natural language query processing
- Context-aware responses
- Multi-turn conversations
- Result synthesis and explanation

### 2. Grant Discovery
- 200,000+ indexed grant programs
- Federal, state, and utility programs
- Real-time updates (daily refresh)
- Location-aware filtering

### 3. Eligibility Checking
- Automated requirements verification
- Multi-criteria evaluation
- Confidence scoring
- Gap analysis

### 4. Compliance Verification
- NEVI (National Electric Vehicle Infrastructure) standards
- CFI (Charging and Fueling Infrastructure) requirements
- State-specific regulations
- Safety and accessibility standards

### 5. Funding Calculations
- Automated rebate calculations
- Stacking multiple programs
- Budget optimization
- ROI projections

## Architecture Highlights

### Tool Orchestration Pattern

```typescript
// Generic pattern (actual implementation uses 12 proprietary tools)
interface Tool {
  name: string;
  description: string;
  execute: (input: any) => Promise<ToolResult>;
}

class AVAAgent {
  private tools: Tool[];

  async processQuery(userQuery: string): Promise<Response> {
    // 1. Analyze query with Claude
    const intent = await this.analyzeIntent(userQuery);

    // 2. Select appropriate tools
    const selectedTools = this.selectTools(intent);

    // 3. Execute tools in parallel or sequence
    const results = await this.executeTools(selectedTools);

    // 4. Synthesize final response
    return this.synthesizeResponse(results, userQuery);
  }
}
```

### Real-time Streaming

```typescript
// WebSocket streaming for instant user feedback
websocket.on('message', async (query) => {
  const stream = await claude.messages.stream({
    model: 'claude-sonnet-4',
    messages: [{ role: 'user', content: query }],
    tools: availableTools
  });

  for await (const chunk of stream) {
    websocket.send(JSON.stringify({
      type: 'delta',
      content: chunk
    }));
  }
});
```

### Automated Updates

```javascript
// n8n workflow (simplified)
Schedule: Daily at 2:00 AM
  ├── Fetch new grants from Grants.gov API
  ├── Check NREL for EV program updates
  ├── Update ComEd incentive amounts
  ├── Sync to PostgreSQL database
  └── Notify via Slack if changes detected
```

## Performance Metrics

- **Response Time:** < 3 seconds (95th percentile)
- **Uptime:** 99.8% (Railway deployment)
- **API Reliability:** 99.5% (retry logic + fallbacks)
- **Grant Coverage:** 200,000+ indexed programs
- **User Satisfaction:** $500/month recurring (100% retention)

## Deployment

### Railway Configuration

```yaml
# Railway.json (simplified)
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Health Monitoring

```typescript
app.get('/health', (req, res) => {
  const health = {
    uptime: process.uptime(),
    database: await checkDatabaseConnection(),
    externalAPIs: await checkExternalAPIs(),
    timestamp: Date.now()
  };

  const status = health.database && health.externalAPIs ? 200 : 503;
  res.status(status).json(health);
});
```

## Security

- **API Key Authentication:** Secure client access
- **Rate Limiting:** Prevent abuse
- **Input Validation:** Sanitize all user input
- **HTTPS/TLS:** Encrypted transport
- **No PII Storage:** Privacy-first design
- **SOC 2 Compliant:** Railway hosting

## Integration Examples

### NREL API Integration

```typescript
// Generic pattern for external API integration
async function fetchNRELData(location: string) {
  const response = await fetch(
    `https://developer.nrel.gov/api/alt-fuel-stations/v1.json?location=${location}`,
    {
      headers: { 'X-Api-Key': process.env.NREL_API_KEY }
    }
  );

  return response.json();
}
```

### Grants.gov Search

```typescript
// Simplified grant search pattern
async function searchGrants(criteria: SearchCriteria) {
  // 1. Build query
  const query = buildGrantsGovQuery(criteria);

  // 2. Execute search
  const results = await grantsGovClient.search(query);

  // 3. Filter and rank
  return rankResults(results, criteria);
}
```

## Code Quality

- **Test Coverage:** 100% on critical paths
- **Type Safety:** Full TypeScript implementation
- **Linting:** ESLint + Prettier
- **Documentation:** JSDoc comments
- **Error Handling:** Comprehensive try/catch
- **Logging:** Structured logging (Winston)

## Lessons Learned

### What Worked Well
✅ WebSocket streaming provided excellent UX
✅ Claude tool use was highly accurate
✅ Railway deployment was seamless
✅ n8n automation saved significant manual work
✅ PostgreSQL handled scale without issues

### Challenges Overcome
🔧 External API rate limits → Implemented caching + retry logic
🔧 Complex eligibility rules → Built rule engine
🔧 Data freshness → Automated daily updates
🔧 Response time → Parallel tool execution

## Future Enhancements

- [ ] Multi-language support (Spanish)
- [ ] Mobile app
- [ ] PDF report generation
- [ ] Historical trend analysis
- [ ] Predictive grant alerts

## Client Testimonial

> "AVA has transformed our grant research process. What used to take days now takes minutes, and we're finding programs we never knew existed. The ROI is incredible."
>
> — Lori, Law Ventures LTD

## Related Projects

- [ADEV Dashboard](../adev-dashboard/) - Multi-agent orchestration platform
- [Code Samples](../../code-samples/) - Reusable patterns

---

**Note:** This documentation showcases the architecture and approach without exposing proprietary code or client-specific business logic. For live demonstrations or detailed technical discussions, please contact me directly.
