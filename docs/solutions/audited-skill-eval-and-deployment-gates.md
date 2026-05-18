---
type: solution
date: 2026-05-04
status: current
tags: [skills, evals, deployment, security, quality]
---

# Audited Skill Eval And Deployment Gates

## Problem

An AI engineering workflow can look polished while still failing in real sessions.

File validation proves the repository shape is correct. It does not prove that:

- skills trigger at the right time
- agents follow the skill under pressure
- tool integrations load the right bootstrap
- users get the expected workflow in a clean session
- deployment is safe enough for public use

## Solution

Treat skills and integrations as behaviour that needs tests.

Use three gates:

1. Structure gate
   - Files, frontmatter, templates, memory index, secrets, and compatibility files are valid.

2. Behaviour gate
   - Natural prompts and explicit skill requests trigger the expected skill.
   - Pressure scenarios show the agent does not rationalise around the rule.

3. Deployment gate
   - A clean session in each target tool routes a normal request into the expected ForgeLoop workflow.
   - Each target has a last verified date, limitations, and setup notes.

## Why This Works

It separates "installed" from "working".

A repository can have perfect files and still fail because the agent never loads the right instruction. Behaviour gates catch that gap before users do.

## Use When

- preparing an open source release
- adding a new skill
- changing a behaviour-shaping skill
- adding a new AI coding tool target
- making a public quality or token-saving claim

## Do Not Use When

- the change is a typo-only docs edit
- the change is pure formatting with no behavioural effect
- the integration is explicitly experimental and labelled as unverified

## Validation

- Run file validation first.
- Run skill trigger tests next.
- Run clean-session deployment acceptance last.
- Attach token packet reports when savings are discussed.

## ForgeLoop Application

ForgeLoop should add this pattern as V4.1:

- skill evaluation standard
- deployment acceptance matrix
- `doctor` command
- verification-before-completion skill
- stricter contribution gates

