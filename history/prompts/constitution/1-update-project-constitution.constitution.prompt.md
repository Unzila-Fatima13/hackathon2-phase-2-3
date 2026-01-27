---
id: 1
title: Update-project-constitution
stage: constitution
date: 2026-01-21
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: m.anas
command: /sp.constitution
labels: ["constitution", "setup", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
You are Claude Code acting as an autonomous full-stack engineer.

You MUST follow Spec-Kit Plus spec-driven development strictly.

Rules:
- No manual coding by the user is allowed
- All implementation must strictly follow specs under /specs
- Always read relevant specs before implementing
- Use the Agentic Dev Stack workflow:
  1. Read spec
  2. Generate plan
  3. Break into tasks
  4. Implement iteratively
- Respect monorepo structure
- Backend and frontend must be implemented together when required

Project Constraints:
- Full-Stack Web Application (NOT CLI)
- Multi-user support with authentication
- REST API secured with JWT
- Persistent storage using Neon Serverless PostgreSQL
- Authentication using Better Auth (frontend) + JWT verification (backend)
- Tech Stack is FIXED and NON-NEGOTIABLE

Tech Stack:
- Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth with JWT
- Repo Type: Monorepo with Spec-Ki
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with specific principles and requirements based on the user input. The new constitution includes:

- Spec-Driven Development principle
- Fixed Tech Stack Compliance principle
- Full-Stack Implementation principle
- Agentic Dev Workflow principle
- Monorepo Structure principle
- No Manual Coding principle

The constitution now clearly defines the technology constraints and development workflow as specified by the user.

## Outcome

- ✅ Impact: Updated project constitution with specific principles aligned to user requirements
- 🧪 Tests: none
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Continue with spec-driven development workflow
- 🧠 Reflection: Constitution now serves as the authoritative guide for project development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation based on constitution