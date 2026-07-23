# 🤖 AGENTS.md — Agent Profiles & Capabilities

> Both agents reference this. Updated when capabilities change.

---

## HERMES (Back-end Brain)

| Field | Value |
|-------|-------|
| **ID** | `hermes` |
| **Role** | Security & Intelligence Orchestrator |
| **Tenant** | `3b2d5d49` |
| **Skills** | 528 loaded |
| **Key Tools** | orchestrator.py, searchdog, spacepirate-intel, cyberpunk_intel.py |
| **Memory** | Session search (FTS5), persistent memory store, MEMORY.md |
| **Strengths** | Vuln scanning, validation, OSINT, cron automation, report generation |
| **Weaknesses** | gog broken (no Sheets write), key masking blocks secret management, no browser auth |
| **FreeRide** | Port 11343, 134 models (OpenRouter + HuggingFace) |
| **Mesh** | `mesh task`, `mesh watch`, `mesh status` |

### Hermes Responsibilities:
1. **Cyberpunk Pipeline** — Target ingestion → scanning → validation → report generation
2. **OSINT Collection** — Space Pirate intel, CISA KEV monitoring, NVD tracking
3. **Cron Management** — 12 cron jobs, all monitored and maintained
4. **Memory Maintenance** — Update MEMORY.md, LEARNINGS.md, PROCESS_REGISTRY.md
5. **Delegation** — Send browser/Sheets tasks to OpenClaw via mesh
6. **Verification** — Verify OpenClaw's Sheets writes and platform submissions

---

## OPENCLAW (Front-end Brain)

| Field | Value |
|-------|-------|
| **ID** | `openclaw-agent` |
| **Role** | Platform & Revenue Executor |
| **Tenant** | `3b2d5d49` (same as Hermes) |
| **Skills** | 232 agency agents + 121 security/forensics skills (353+ total) |
| **Key Tools** | gog (Sheets/Docs/Calendar write), Playwright (browser), 232 agency agents |
| **Memory** | CONTEXT.md, daily notes, episodic/semantic/procedural memory |
| **Strengths** | Browser automation, platform auth, Sheets write, form submission, content publishing |
| **Weaknesses** | No deep vuln analysis skills, limited OSINT capabilities |
| **FreeRide** | Own instance (OpenRouter models) |
| **Mesh** | Same tenant, receives mesh tasks from Hermes |

### OpenClaw Responsibilities:
1. **Platform Submission** — Login to HackerOne/Bugcrowd, fill forms, submit reports
2. **Revenue Tracking** — Write all submissions to Sheets, track payouts
3. **Google Sheets** — Maintain Dashboard, Submissions, Payouts, Live Intel, Targets tabs
4. **Content Publishing** — Cashcow Pinterest, social media, content distribution
5. **Browser Automation** — Any web-based automation requiring auth state
6. **Agency Agents** — 232 on-demand specialist agents for any domain

---

## HANDOFF PROTOCOL

### When to Delegate:
| If you need... | Delegate to... | Command |
|---|---|---|
| Write to Google Sheets | OpenClaw | `mesh task → openclaw-agent` |
| Login to website | OpenClaw | `mesh task → openclaw-agent` |
| Fill web form | OpenClaw | `mesh task → openclaw-agent` |
| Browser automation | OpenClaw | `mesh task → openclaw-agent` |
| Deep vuln analysis | Hermes | `mesh task → hermes` |
| OSINT research | Hermes | `mesh task → hermes` |
| Report generation | Hermes | `mesh task → hermes` |
| Mass scanning | Hermes | `mesh task → hermes` |

### Task Format:
```
Title: [Action verb] [object]
Description: [Clear instruction with expected output]
Priority: [high/medium/low]
Skills Required: [list of skills]
Tools Needed: [playwright, gog, bitwarden, etc.]
Expected Output: [what success looks like]
Fallback: [alternative if blocked]
```

### 🤝 Skills-First Handshake Protocol (MANDATORY)
Full protocol: `/opt/data/shared/crew-os/SKILLS-FIRST-HANDSHAKE-PROTOCOL.md`

**Summary:**
1. Hermes sends task with skills/tools declared
2. OpenClaw audits own capabilities → accepts/rejects with constraints
3. OpenClaw executes → sends progress every 15 min
4. Hermes verifies output
5. Silent failure is prohibited — stuck >5 min = alert
6. Both log to memory + Sentry

### Verification Protocol:
1. After mesh task assigned → check status
2. After OpenClaw writes to Sheets → Hermes verifies with `gws sheets get`
3. After submission → Hermes confirms via platform API or email
4. All findings → Sentry with evidence links

---

## CAPABILITY MATRIX

| Capability | Hermes | OpenClaw | Notes |
|------------|--------|----------|-------|
| Web search | ✅ | ✅ | Both have |
| Browser automation | ⚠️ limited | ✅ primary | OpenClaw has auth state |
| Sheets write | ❌ | ✅ | Hermes gog broken |
| Sheets read | ✅ (gws) | ✅ | Both work |
| Vuln scanning | ✅ | ❌ | Hermes primary |
| Report generation | ✅ | ❌ | Hermes primary |
| Form submission | ❌ | ✅ | OpenClaw primary |
| Platform auth | ❌ | ✅ | OpenClaw primary |
| OSINT | ✅ | ❌ | Hermes primary |
| Content publishing | ❌ | ✅ | OpenClaw primary |
| Cron management | ✅ | ✅ | Both should maintain |
| Memory management | ✅ | ✅ | Separate stores, shared MEMORY.md |
| LLM calls | ✅ (FreeRide) | ✅ (FreeRide) | Separate instances |
| Mesh communication | ✅ | ✅ | Same tenant |

---

## 📋 PROPER ARCHITECTURE DOC
**Read this first:** `/opt/data/shared/crew-os/PROPER-ARCHITECTURE.md`
It defines: skill assignments by workflow, memory architecture, loop engineering, mesh protocol, dedup plan.

## DEFAULT SKILLS (Both Agents — Load for Every Session)

These skills MUST be loaded and used by default for all tasks:

### Thinking/Planning Stack
- **oracle** — First-principles assumption auditor
- **understand-anything** — Scan systems/codebases before making changes
- **fable-mode** — Stage-map + verify before shipping
- **harness** — Agent team architecture (Crew OS, Phase 0-7)
- **loop-engineering** — CI sweeps, changelog, post-merge cleanup
- **agentic-planning** — Structured planning before implementation
- **brainstorming** — Before creative/constructive work

### Business Stack
- **monetize** — Pricing, packaging, money models
- **money-playbook** — Legacy monetization playbook
- **ceo-advisor** — Strategic decisions
- **pricing-strategy** — Pricing design

### Security/Production Stack
- **agents-towards-production** — Production-ready patterns
- **karakeep** — Persistent searchable memory
- **sentry-cli** — Error tracking system-wide

### Default Workflow
1. Load understand-anything → scan existing system
2. Load fable-mode → stage-map the work
3. Load harness → check if agent team can parallelize
4. Execute with verification at each stage
5. Send events to Sentry for monitoring

### Shared Resources
- **Bitwarden vault**: Both agents have access (bw CLI, master password in .keyring_pass)
- **Platform cookies**: OpenClaw has all platform cookies (work-archive)
- **Mesh**: Bidirectional, same tenant (3b2d5d49), workspace "hermes-openclaw-bridge"
- **FreeRide**: Both have separate instances on port 11343

---

## SWARM SKILLS (Both Agents — Hella Swarm Skills Available)

We have MASSIVE swarm/orchestration capabilities. Key swarm skills on both agents:

### Hermes Swarm Skills
- `agent-swarm` — OpenRouter-based multi-agent routing
- `agent-team-orchestration` — Define roles, task lists, parallel execution
- `agentic-engineering` — Eval-first execution with autonomous loops
- `multi-agent-architect` — Design multi-agent systems
- `multi-agent-patterns` — Patterns for parallel/collaborative work
- `multi-agent-task-orchestrator` — Route tasks to specialized agents
- `dispatching-parallel-agents` — Run 2+ independent tasks concurrently
- `parallel-agents` — Multi-agent orchestration patterns
- `subagent-driven-development` — Execute plans via sub-agents
- `subagent-orchestrator` — Coordinate quota-aware parallel sub-agents
- `harness` — Full agent team architecture (Phase 0-7)

### OpenClaw Swarm Skills
- `agents-orchestrator` — Meta-skill for all agents
- `agent-evaluation` — Test and benchmark agents
- `agent-manager-skill` — Manage multiple CLI agents
- `agent-memory-systems` — Memory for intelligent agents
- `agent-phone-call` — Voice agents
- `agentic-identity-trust-architect` — Identity systems
- `swarm_scout` — System health monitoring
- 232 agency agents available for any domain

### Swarm Usage Pattern
1. Hermes finds vulns → dispatches OpenClaw for parallel submission
2. OpenClaw publishes content → Hermes verifies analytics
3. Both monitor FreeRide, Sentry, and mesh health independently
4. Cross-agent verification: Hermes verifies Sheets writes, OpenClaw verifies submissions

---

*Last updated: 2026-06-28 after system audit, watchdog fix, and skills standardization*
