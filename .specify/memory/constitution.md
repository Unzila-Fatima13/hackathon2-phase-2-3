<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All principles and sections based on user requirements
Removed sections: N/A
Templates requiring updates: ⚠ pending review of .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
All development must follow Spec-Kit Plus spec-driven development methodology; No implementation without corresponding specifications under /specs; Implementation must strictly adhere to defined specs

### Fixed Tech Stack Compliance
Technology stack is FIXED and NON-NEGOTIABLE: Next.js 16+ App Router with TypeScript and Tailwind CSS for frontend; Python FastAPI with SQLModel ORM for backend; Neon Serverless PostgreSQL for persistence; Better Auth with JWT for authentication

### Full-Stack Implementation
Backend and frontend must be developed together when required; Applications must support multi-user functionality with proper authentication; REST APIs must be secured with JWT tokens

### Agentic Dev Workflow
Follow Agentic Dev Stack workflow: Read spec → Generate plan → Break into tasks → Implement iteratively; Always read relevant specs before implementing; Respect monorepo structure

### Monorepo Structure
Respect monorepo architecture with proper separation of concerns; Maintain consistent code organization across frontend and backend; Follow established patterns for cross-cutting concerns

### No Manual Coding
No manual coding by the user is allowed; All implementation must be performed through automated processes following specs; Human intervention limited to specification and review

## Technology Constraints
Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS; Backend: Python FastAPI; ORM: SQLModel; Database: Neon Serverless PostgreSQL; Auth: Better Auth with JWT verification; Repo Type: Monorepo

## Development Workflow
Strict adherence to Agentic Dev Stack workflow; All implementation must follow specs under /specs; Backend and frontend developed together when required; Code must be testable and maintainable

## Governance
Constitution supersedes all other practices; All implementation must comply with specified tech stack and methodology; Amendments require formal documentation and approval; All changes must follow spec-driven approach

**Version**: 1.0.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21