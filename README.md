# Agentic Reliability Lab

**A spec-driven engineering reference implementation for inspectable agent-style workflows.**

[![CI](https://github.com/sc-aisuperjack/agentic-reliability-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/sc-aisuperjack/agentic-reliability-lab/actions/workflows/ci.yml)

> **Transparent mode:** This project starts with a deterministic policy engine, **not an LLM-powered autonomous agent**. It executes actual Python routing, tenant-scoped synthetic retrieval, order lookup and safety checks. It does not use external model keys, real customer data or proprietary Vozara/Centrica code.

## Included

- React + TypeScript interface: customer scenarios, agent execution trace, synthetic tenant selection, evaluation results and requirements.
- FastAPI backend with typed contracts and inspectable tool decisions.
- Versioned 14-case behavioural evaluation suite and pytest.
- SDD documents: intent, specification, implementation plan and architectural decision.
- GitHub Actions quality gates, plus Render Blueprint with free-tier resource requests.

## Architecture

~~~mermaid
flowchart TD
    UI[React Static Site] -->|HTTPS| API[FastAPI Backend]
    API --> ORCH[Policy-based Orchestrator]
    ORCH --> KB[Synthetic Knowledge]
    ORCH --> ORDERS[Synthetic Orders]
    ORCH --> GUARDS[Safety and Validation]
    API --> EVAL[Versioned Evaluations]
    CI[GitHub Actions] --> EVAL
    CI --> TESTS[pytest and TypeScript]
~~~

## Run locally

Requires Python 3.11+ and Node.js 20+.

Backend:

~~~bash
cd backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --reload --port 8000
~~~

API docs at http://localhost:8000/docs.

Frontend, in a separate terminal:

~~~bash
cd frontend
npm install
npm run dev
~~~

Open http://localhost:5173. The frontend uses VITE_API_URL if set; otherwise it calls localhost:8000. See frontend/.env.example.

## Render deployment

The render.yaml Blueprint requests two services: a free Python Web Service named agentic-reliability-api and a static site named agentic-reliability-lab. Import it in Render Dashboard and **inspect quoted pricing before approving any plan**. The free backend sleeps when idle, leading to a cold-start delay.

If Render assigns different service URLs, update VITE_API_URL in the static site's build settings and CORS_ORIGINS in the backend service to match. Both frontend and backend must be reachable.

## Spec-driven engineering

- [Intent](intent/reliable-support/intent.md): Why.
- [Specification](intent/reliable-support/spec.md): What and acceptance criteria.
- [Plan](intent/reliable-support/plan.md): How and proof.
- [ADR](docs/adr/001-deterministic-baseline.md): Architecture trade-offs.
- [Evaluation source](backend/app/evaluations.py): Executable behavioural cases.

## Limitations

Fictional businesses and records only. The public tenant selector is not real authentication. Known-phrase safety rules do not solve general prompt injection. Document identifiers are verified against selected knowledge but not semantically scored. No real handoffs or LLM calls occur.

## Next development milestone

Add an optional LLM reasoning adapter behind controlled tools with budgets, prompt-injection evaluations and accurate trace/usage reporting. Default public mode remains free.

## Copyright

No open-source licence has been granted yet; source is public for review, not unrestricted reuse.
