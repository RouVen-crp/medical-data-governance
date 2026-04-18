# Project: dataMine

## Overview
A project for data mining and analysis.

## Tech Stack
*To be defined*

## Core Mandates
- **Skill Visibility:** Do not display the full list of available skills when the user requests help or project summaries. Keep the interface clean and focused.
- **Language:** Always respond in Simplified Chinese.

## Behavioral Guidelines

These guidelines are designed to reduce common LLM coding mistakes and prioritize caution over speed.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- Before implementing, state assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them instead of picking silently.
- If a simpler approach exists, suggest it. Push back when warranted.
- If something is unclear, stop and ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No unrequested "flexibility" or "configurability".
- No error handling for impossible scenarios.
- If 200 lines can be 50, rewrite it.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style perfectly.
- Remove orphans created by *your* changes (imports, variables, functions).
- Do not remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
- Transform tasks into verifiable goals (e.g., "Write a test that reproduces the bug, then make it pass").
- For multi-step tasks, state a brief plan with verification steps.
1. [Step] ¡ú verify: [check]
2. [Step] ¡ú verify: [check]
3. [Step] ¡ú verify: [check]
---

**Success Metric:** These guidelines are working if there are fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation.
