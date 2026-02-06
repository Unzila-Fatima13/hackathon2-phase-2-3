---
id: "0001"
title: "Fix Vercel Deploy"
stage: "general"
date: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-fullstack-todo-app"
user: "m.anas"
command: "manual"
labels: ["vercel", "deployment", "monorepo", "nextjs", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "vercel.json"
  - "frontend/package.json"
  - "package.json"
tests: []
---

# Fix Vercel Deployment Issues

## Context
The user had a Vercel deployment failing for their fullstack todo application. The project is structured as a monorepo with a frontend directory containing a Next.js application.

## Problem
Vercel deployment was failing with error during the build phase. Logs showed Next.js security vulnerability warnings and the build wasn't completing successfully in the Vercel environment.

## Solution Applied
1. Updated Vercel configuration (`vercel.json`) to properly handle the monorepo structure with the correct rootDirectory and build commands
2. Upgraded Next.js version from 14.0.4 to ^14.2.20 to address security vulnerability
3. Updated eslint-config-next to match the Next.js version
4. Modified the vercel-build script to use `npm ci` instead of `npm install` for consistent dependency installation

## Changes Made
- Modified vercel.json to use framework-level configuration with proper rootDirectory
- Updated Next.js dependency in frontend/package.json
- Updated eslint-config-next dependency in frontend/package.json
- Improved vercel-build script in root package.json

## Verification
- Ran local build successfully with `npm run build`
- Confirmed Next.js build completed without errors

## Outcome
The Vercel deployment configuration is now properly set up for the monorepo structure, and the Next.js security vulnerability has been addressed by upgrading to a patched version.

## Files Modified
- vercel.json: Updated to properly configure Vercel for monorepo
- frontend/package.json: Upgraded Next.js to address security issue
- package.json: Improved vercel-build script

## Next Steps
Push the changes to GitHub and redeploy on Vercel to verify the deployment succeeds.

## Reflection
The main issue was that the original Vercel configuration didn't properly account for the monorepo structure, and the outdated Next.js version had a known security vulnerability that needed to be addressed.

Failure modes observed: None
Next experiment to improve prompt quality: N/A