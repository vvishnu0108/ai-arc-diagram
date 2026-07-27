# Architect Studio — Standard Operating Procedure (SOP)

**Version:** 1.2 · **Last updated:** February 2026
**Audience:** Engineers deploying Architect Studio on their own machine or private server.

Architect Studio is an MCP-native Cloud Architecture Copilot. It combines NVIDIA NIM LLM reasoning with real Microsoft Learn + AWS Knowledge MCP servers and a `diagrams` → `graphviz2drawio` pipeline to produce production-grade Azure/AWS architecture diagrams with official cloud icons rendered inside an embedded draw.io editor.

---

## 1. Table of Contents

1. [System Requirements](#2-system-requirements)
2. [Third-party Accounts & Credentials](#3-third-party-accounts--credentials)
3. [Get the Code](#4-get-the-code)
4. [Backend Setup](#5-backend-setup)
5. [Frontend Setup](#6-frontend-setup)
6. [Environment Variables Reference](#7-environment-variables-reference)
7. [Start the Application](#8-start-the-application)
8. [Verify the Installation](#9-verify-the-installation)
9. [User Guide](#10-user-guide)
10. [API Reference](#11-api-reference)
11. [Troubleshooting](#12-troubleshooting)
12. [Upgrading & Maintenance](#13-upgrading--maintenance)

---

## 2. System Requirements

**Operating System**
- Ubuntu 22.04 / Debian 12 (recommended)
- macOS 13+ (Apple Silicon or Intel)
- Windows 10/11 via WSL2 (Ubuntu)

**Runtime**
- Python **3.11+** (3.11 tested, 3.12 supported)
- Node.js **18 LTS+** (20 recommended)
- Yarn **1.22+** (npm is **not** supported)
- Graphviz **2.42+** (system binary — `dot` must be on PATH)
- MongoDB is **not required** (v1.x uses in-memory sessions)

**Hardware**
- 4 GB RAM minimum, 8 GB recommended
- 3 GB free disk space
- Stable internet connection (backend calls NVIDIA NIM + MCP servers over HTTPS)

**Network egress must reach:**
- `https://integrate.api.nvidia.com` (NVIDIA NIM API)
- `https://learn.microsoft.com` (Microsoft Learn MCP)
- `https://knowledge-mcp.global.api.aws` (AWS Knowledge MCP)
- `https://embed.diagrams.net` (draw.io iframe — served to the user's browser)

---

## 3. Third-party Accounts & Credentials

You need **one credential**: a NVIDIA NIM API key.

1. Sign up at <https://build.nvidia.com/> (free tier available).
2. In your NVIDIA account, generate an API key (starts with `nvapi-…`).
3. Confirm the model you'll use is available on your tier. The default is `openai/gpt-oss-120b`. Alternatives: `meta/llama-3.1-70b-instruct`, `meta/llama-3.1-8b-instruct`.

Microsoft Learn MCP and AWS Knowledge MCP are **public, no auth needed**.

---

## 4. Get the Code

```bash
# 4.1 Clone or unpack the project
git clone <your-repo-url> architect-studio
cd architect-studio

# 4.2 Project layout
architect-studio/
├── backend/          # FastAPI service (Python)
├── frontend/         # React CRA app (Node)
├── memory/           # Architecture notes & PRD (optional)
└── SOP.md            # This document
```

---

## 5. Backend Setup

### 5.1 Install system packages (once per machine)

**Ubuntu / Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip \
                        graphviz libgraphviz-dev pkg-config
```

**macOS (Homebrew):**
```bash
brew install python@3.11 graphviz
```

**Windows (WSL Ubuntu):** identical to Ubuntu commands above.

Verify:
```bash
python3 --version    # ≥ 3.11
dot -V               # graphviz version 2.42+
```

### 5.2 Create a Python virtualenv & install dependencies

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate           # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Key packages installed: `fastapi`, `uvicorn`, `langchain-openai`, `mcp`, `diagrams`, `graphviz2drawio`, `sse-starlette`, `httpx`, `python-dotenv`.

### 5.3 Configure `backend/.env`

Create `backend/.env` (or edit the existing file). Minimal contents:

```ini
# --- LLM (NVIDIA NIM) ---
llm_api_key="nvapi-REPLACE-WITH-YOUR-KEY"
llm_api_base_url="https://integrate.api.nvidia.com/v1"
llm_model_name="openai/gpt-oss-120b"
llm_temperature="0.2"
llm_max_tokens="8192"
llm_timeout="180"
llm_max_retries="2"

# --- MCP (public endpoints, no auth) ---
MS_LEARN_MCP_URL="https://learn.microsoft.com/api/mcp"
AWS_KNOWLEDGE_MCP_URL="https://knowledge-mcp.global.api.aws"
MCP_TIMEOUT="25"

# --- CORS ---
CORS_ORIGINS="*"

# --- MongoDB (kept for future persistence; not used in v1) ---
MONGO_URL="mongodb://localhost:27017"
DB_NAME="architect_studio"
```

⚠ **Do not commit `.env` to version control.** Add `backend/.env` to `.gitignore`.

---

## 6. Frontend Setup

```bash
cd ../frontend
yarn install
```

### 6.1 Configure `frontend/.env`

```ini
# Point the frontend at the backend base URL WITHOUT the /api suffix.
# Local dev:
REACT_APP_BACKEND_URL=http://localhost:8001

# When deploying, replace with the public URL where the backend is reachable, e.g.
# REACT_APP_BACKEND_URL=https://architect.example.com
```

**Important:** the frontend always prefixes API calls with `/api`, so `REACT_APP_BACKEND_URL` must be the **host only**, no trailing `/api`.

### 6.2 (Optional) Apply your own Lenovo/brand theme

Drop your custom CSS variables into `frontend/src/styles/lenovo-overrides.css`. This file is imported after `index.css` so it wins. Example:

```css
:root {
    --primary: 0 79% 50%;           /* Lenovo red */
    --background: 0 0% 99%;
}
.dark {
    --background: 240 6% 6%;
}
```

---

## 7. Environment Variables Reference

### `backend/.env`

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `llm_api_key` | **Yes** | — | NVIDIA NIM API key (`nvapi-…`) |
| `llm_api_base_url` | Yes | `https://integrate.api.nvidia.com/v1` | NIM endpoint |
| `llm_model_name` | Yes | `openai/gpt-oss-120b` | LLM model id |
| `llm_temperature` | No | `0.2` | Sampling temperature |
| `llm_max_tokens` | No | `8192` | Max output tokens |
| `llm_timeout` | No | `180` | Per-request LLM timeout (seconds) |
| `llm_max_retries` | No | `2` | LLM retry attempts |
| `MS_LEARN_MCP_URL` | No | Microsoft Learn URL | Override MS Learn MCP endpoint |
| `AWS_KNOWLEDGE_MCP_URL` | No | AWS Knowledge URL | Override AWS Knowledge MCP endpoint |
| `MCP_TIMEOUT` | No | `25` | MCP HTTP timeout (seconds) |
| `CORS_ORIGINS` | No | `*` | Comma-separated allowed origins |
| `MONGO_URL` | No | Not used in v1 | Reserved for future persistence |

### `frontend/.env`

| Variable | Required | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | **Yes** | Backend host root (no `/api` suffix) |

---

## 8. Start the Application

### 8.1 Local development (two terminals)

**Terminal 1 — Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
yarn start
```

Open <http://localhost:3000> in a modern browser (Chrome, Edge, Firefox, Safari).

### 8.2 Production start (single machine, background)

Recommended process manager: `supervisord`, `pm2`, or `systemd`.

**Example systemd unit (`/etc/systemd/system/architect-backend.service`):**
```ini
[Unit]
Description=Architect Studio backend
After=network.target

[Service]
User=architect
WorkingDirectory=/opt/architect-studio/backend
EnvironmentFile=/opt/architect-studio/backend/.env
ExecStart=/opt/architect-studio/backend/.venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001 --workers 2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Frontend for production:
```bash
cd frontend
yarn build          # outputs to frontend/build/
# Serve the static folder behind an nginx reverse-proxy that also
# forwards /api to the backend on port 8001.
```

**Minimal nginx block:**
```nginx
server {
    listen 80;
    server_name architect.example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_read_timeout 600s;      # allow long diagram jobs
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        root /opt/architect-studio/frontend/build;
        try_files $uri /index.html;
    }
}
```

---

## 9. Verify the Installation

### 9.1 Backend health
```bash
curl http://localhost:8001/api/health
# {"status":"healthy"}
```

### 9.2 MCP connectivity
```bash
curl http://localhost:8001/api/mcp/sources
# Expect JSON showing both `ms_learn` and `aws_knowledge` as "online".
```

### 9.3 End-to-end generation (async, no timeout risk)
```bash
JOB=$(curl -s -X POST http://localhost:8001/api/architecture/generate/async \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Azure AKS microservices multi-region",
    "intake":{"cloud_provider":"azure","architecture_type":"microservices","kubernetes":true,"data_layer":"sql","high_availability":true,"monitoring":true},
    "clarification_answers":{}
  }')
JOB_ID=$(echo "$JOB" | python3 -c "import sys,json;print(json.load(sys.stdin)['job_id'])")

# Poll until complete
while true; do
    STATUS=$(curl -s http://localhost:8001/api/architecture/jobs/$JOB_ID)
    STAGE=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['status'],d['stage'],d['progress'])")
    echo "$STAGE"
    echo "$STATUS" | grep -q '"status": "complete"' && break
    echo "$STATUS" | grep -q '"status": "error"' && break
    sleep 3
done
```

Expected: reaches `complete 100%` in 20–90 s and the response contains a `drawio_xml` payload with embedded base64 Azure icons.

### 9.4 Open the UI

Visit `http://localhost:3000`. You should see:
- **Architect Studio** brand mark (red **A**) in the top-left
- **14 pre-built templates** in the left sidebar
- **Microsoft Learn MCP** and **AWS Knowledge MCP** both showing **ONLINE**
- Theme toggle (sun/moon) in the top-right

---

## 10. User Guide

### 10.1 One-shot generation (template)
1. Click any template in the left sidebar (e.g. *Azure Microservices on AKS*).
2. Adjust the prompt / intake if needed.
3. Click **Generate Architecture**.
4. Loading overlay shows staged progress (`Retrieving MCP knowledge → NIM reasoning → Rendering diagram`). Typical time: **20–60 s**.
5. When done, the workspace opens with:
   - **Reasoning Timeline** (left rail) — AI decisions with confidence + MCP citations
   - **Draw.IO Canvas** (center) — real Azure/AWS icons, editable
   - **Refinement Chat** (bottom) — iterate with plain English
   - **Context Panel** (right) — metadata, validation, tradeoffs, security/cost/scalability recommendations, MCP snippets

### 10.2 Guided (with clarifications)
If your prompt is sparse, Architect Studio asks 3–6 clarification questions (traffic scale, HA, data layer, etc.). Answer, click **Generate Architecture**.

### 10.3 Refinement chat commands (quick actions)
- **Add monitoring** — layer in observability
- **Optimize cost** — swap for cheaper SKUs, add lifecycle policies
- **Multi-region** — active-active with global routing
- **Harden security** — WAF, private endpoints, CMK, zero-trust
- **Add DR** — cross-region replication, RPO/RTO targets

Or type free-form: *"Add a Redis caching layer between AKS and Cosmos DB"*.

### 10.4 Snapshots & Export
Inside the draw.io canvas toolbar:
- **History icon** — Save the current diagram as a snapshot; list & one-click restore any previous version.
- **Download icon** — Export as **PNG**, **SVG**, or download the raw `.drawio` file.
- **Fullscreen icon** — Distraction-free canvas.

### 10.5 Focus mode
Click **Focus** in the header to hide both sidebars and give the canvas the full viewport.

### 10.6 Theme toggle
Click the **Sun / Moon** icon in the header. Preference persists in localStorage. Draw.io iframe re-syncs to the new theme.

---

## 11. API Reference

Base URL: `${REACT_APP_BACKEND_URL}/api`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Liveness probe |
| GET | `/mcp/sources` | List MCP servers + tool availability |
| GET | `/architecture/templates` | 14 pre-built templates |
| POST | `/architecture/intent` | Extract structured intake from a free-text prompt |
| POST | `/architecture/clarify` | Get clarification questions for a sparse intake |
| **POST** | **`/architecture/generate/async`** | **Kick off generation (returns `job_id` immediately)** |
| **POST** | **`/architecture/refine/async`** | **Kick off refinement (returns `job_id`)** |
| **GET** | **`/architecture/jobs/{job_id}`** | **Poll job status (stage, progress, result)** |
| POST | `/architecture/generate` | Synchronous generation (only use if you can wait ~90 s) |
| POST | `/architecture/refine` | Synchronous refinement |
| POST | `/architecture/generate/stream` | SSE variant (may hit 60 s proxy timeouts) |
| GET | `/architecture/sessions` | List recent sessions |
| GET | `/architecture/{session_id}` | Get a single session with full state |
| POST | `/architecture/{session_id}/snapshots` | Save a version of the current diagram |
| GET | `/architecture/{session_id}/snapshots` | List versions (newest first) |
| POST | `/architecture/{session_id}/snapshots/{snap_id}/restore` | Restore a snapshot |

**Recommended client flow:** always use `/generate/async` + poll `/jobs/{id}` every 1.5–2 s to avoid any proxy streaming timeouts.

---

## 12. Troubleshooting

### 12.1 Backend won't start
- Check logs: `journalctl -u architect-backend -n 100` (systemd) or terminal output.
- Ensure Python 3.11+ and virtualenv is activated.
- If `mcp` or `langchain-openai` are missing: `pip install -r requirements.txt` again.

### 12.2 `/api/mcp/sources` shows both as offline
- Confirm outbound HTTPS to `learn.microsoft.com` and `knowledge-mcp.global.api.aws` is not blocked by a corporate firewall.
- Bump `MCP_TIMEOUT` in `.env` (e.g. `MCP_TIMEOUT=45`).

### 12.3 Generation fails: *"diagrams execution failed"*
- Verify graphviz: `which dot && dot -V`.
- Reinstall: `sudo apt-get install --reinstall graphviz` (or `brew reinstall graphviz`).
- The pipeline auto-repairs ImportErrors from the LLM (wrong casing / wrong module) up to 3 attempts — if all 3 fail, check the error in the response `message` field for details.

### 12.4 Generation hangs / times out
- Try a smaller model temporarily: set `llm_model_name="meta/llama-3.1-8b-instruct"` for a quick smoke test.
- Verify your NVIDIA NIM key: `curl -H "Authorization: Bearer $llm_api_key" https://integrate.api.nvidia.com/v1/models` should return the model catalogue.
- **`meta/llama-3.3-70b-instruct` is currently degraded on NIM** — do not use.
- Increase `llm_timeout` in `.env` if the model is slow but eventually responds.

### 12.5 Frontend can't reach backend / 502 in browser
- Verify `REACT_APP_BACKEND_URL` in `frontend/.env` matches the actual backend host (no trailing `/api`).
- Rebuild the frontend after changing `.env`: `yarn build` (CRA bakes env vars at build time).
- Behind a proxy: raise `proxy_read_timeout` to 600 s (see nginx example).
- Ensure the app is calling **`/generate/async` + polling** (default in this codebase) — the synchronous endpoint can exceed proxy timeouts.

### 12.6 Draw.IO canvas is blank
- The generated `drawio_xml` may not have loaded. Refresh the canvas via the ↻ button in the toolbar.
- Check browser console for postMessage errors from `embed.diagrams.net`. This service must be reachable from the user's browser.

### 12.7 Theme not switching correctly inside the draw.io iframe
- Click the ↻ (refresh) button in the canvas toolbar — the iframe is reloaded and re-syncs.

### 12.8 Snapshots disappear after a restart
- v1 uses in-memory storage. Restarting the backend clears all sessions, snapshots, and MCP context. Persistence to MongoDB is on the roadmap (P2).

---

## 13. Upgrading & Maintenance

### 13.1 Pull latest code
```bash
git pull
cd backend  && source .venv/bin/activate && pip install -r requirements.txt
cd ../frontend && yarn install
sudo systemctl restart architect-backend      # or your chosen supervisor
# Rebuild frontend if you serve the static build:
cd ../frontend && yarn build
```

### 13.2 Rotate the NVIDIA NIM key
Edit `backend/.env`, replace `llm_api_key`, restart the backend. No frontend rebuild needed.

### 13.3 Change the model
Edit `llm_model_name` in `backend/.env`. Verified working models on NIM:
- `openai/gpt-oss-120b` (default — fast, high-quality code gen)
- `meta/llama-3.1-70b-instruct`
- `meta/llama-3.1-8b-instruct` (smallest, fastest, lower quality)

### 13.4 Logs to monitor
- **Backend stdout/stderr** — contains httpx logs for NIM + MCP, plus agent errors.
- **Nginx access/error logs** — request-level issues, proxy timeouts.
- **Browser console** — draw.io postMessage errors, network failures.

### 13.5 Backups (once persistence is added)
Currently there's nothing to back up — everything is ephemeral. Once MongoDB support is enabled, run daily `mongodump` of the `architect_studio` DB.

---

## Appendix A — Quick command cheat sheet

```bash
# Full local start
cd backend && source .venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
cd frontend && yarn start

# Health check
curl -s localhost:8001/api/health

# Generate via curl (async pattern)
curl -s -X POST localhost:8001/api/architecture/generate/async \
  -H "Content-Type: application/json" \
  -d '{"prompt":"AWS EKS three-tier web app","intake":{"cloud_provider":"aws","architecture_type":"microservices","kubernetes":true},"clarification_answers":{}}'

# Poll a job
curl -s localhost:8001/api/architecture/jobs/<job_id> | jq

# Reset everything (in-memory sessions cleared by restart)
sudo systemctl restart architect-backend
```

---

## Appendix B — Architecture flow

```
User prompt + intake
      │
      ▼
POST /api/architecture/generate/async ─► job store (in-memory)
      │                                        │
      ▼                                        ▼
 background asyncio task                emit(stage, message)
      │
      ├─► MCPOrchestrator (parallel)
      │     ├─ Microsoft Learn MCP (HTTP streamable)
      │     └─ AWS Knowledge MCP    (HTTP streamable)
      │
      ├─► NIM analysis LLM call  (reasoning + validation + tradeoffs + recs)
      ├─► NIM diagram-code LLM call (python `diagrams` code)
      │
      ├─► subprocess: python diagrams-code.py → .dot file
      ├─► subprocess: graphviz2drawio → .drawio XML (with base64 Azure/AWS icons)
      │
      ▼
job.result = full GenerateResponse

Client polls GET /jobs/{id} every ~1.5 s until status=complete.
```

---

## Appendix C — File & directory reference

**Backend**
- `backend/server.py` — FastAPI entry, routers, CORS, graphviz auto-install
- `backend/routers/architecture.py` — all architecture endpoints
- `backend/routers/mcp_router.py` — MCP status endpoint
- `backend/services/agent.py` — orchestrates NIM + MCP + diagram exec
- `backend/services/llm.py` — NIM client (langchain-openai)
- `backend/services/mcp/` — MCP HTTP clients + orchestrator + planner
- `backend/services/diagram_generator.py` — python-code execution + graphviz2drawio + auto-repair
- `backend/services/diagram_classes.py` — introspected reference of real `diagrams` classes
- `backend/services/jobs.py` — async job store
- `backend/services/sessions.py` — in-memory session store
- `backend/services/templates.py` — 14 pre-built templates
- `backend/prompts/system_prompt.py` — all LLM prompts

**Frontend**
- `frontend/src/pages/Workspace.js` — main IDE-style layout
- `frontend/src/components/sidebar/{Left,Right}Sidebar.js`
- `frontend/src/components/workspace/{IntakePanel,ClarificationCards,ReasoningTimeline,RefinementChat,CenterWorkspace}.js`
- `frontend/src/components/drawio/{DrawIOCanvas,SnapshotMenu,ExportMenu}.js`
- `frontend/src/components/{validation,tradeoffs,recommendations,mcp,metadata}/*` — right-panel modules
- `frontend/src/store/useArchitectureStore.js` — Zustand global state
- `frontend/src/services/api.js` — axios client + `runAsyncJob()` helper
- `frontend/src/contexts/ThemeContext.js` — light/dark toggle with localStorage
- `frontend/src/index.css` — Lenovo-inspired design tokens (light + dark)
- `frontend/src/styles/lenovo-overrides.css` — **your custom brand tokens here**

---

**End of SOP.** For issues or contributions, open a GitHub issue against the project repo.
