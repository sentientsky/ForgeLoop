---
type: research
status: current
tags: [compatibility, adoption, setup, ai-coding-tools]
---

# AI Coding Tool Adoption Review

Date: 2026-04-26

ForgeLoop should make setup choices based on real usage data, but the market is moving quickly and survey samples differ.

The setup menu therefore uses two ideas:

- support the most useful tools now
- show the rest as coming soon until their native instruction formats are tested

## Data Points

### State of Code 2025

State of Code 2025 reports current AI coding tool usage among its respondents:

| Tool | Usage |
| --- | ---: |
| Claude Code | 57% |
| Cursor | 43% |
| GitHub Copilot | 30% |
| Codex | 23% |
| Antigravity | 14% |
| Lovable | 14% |
| Cline | 11% |
| Zed | 9% |
| Amazon Q Developer | 9% |
| Kiro | 7% |
| Replit | 7% |
| Windsurf | 5% |
| CodeRabbit | 5% |

This source is useful for agentic coding communities, but it may over-represent people already deep in AI coding workflows.

### SonarSource State of Code Developer Survey 2026

The SonarSource report gives a broader software-development view. It reports GitHub Copilot at 75%, ChatGPT at 74%, Claude / Claude Code at 48%, Gemini / Duet AI at 31%, Cursor at 21%, Perplexity at 21%, OpenAI Codex at 17%, JetBrains at 12%, and Amazon Q Developer at 8%.

This source is useful for broader workplace usage, but it mixes coding agents, chat tools, and IDE assistants.

### JetBrains Developer Ecosystem 2025

JetBrains reports that 85% of developers regularly use AI tools for coding and development, and 62% rely on at least one AI coding assistant, agent, or code editor.

This supports the need for ForgeLoop to be tool-portable rather than Claude-only.

### GitHub Coding Agent Adoption Study

A 2026 research paper estimates coding-agent adoption across GitHub projects at 22.20% to 28.66% in the first half of 2025.

This supports treating agentic coding as mainstream enough for repo-level setup files.

## Setup Menu Decision

Supported now:

1. Claude Code
2. Codex
3. Cursor
4. GitHub Copilot
5. All supported tools

Coming soon:

- ChatGPT coding workspace
- Gemini CLI / Gemini Code Assist
- Windsurf
- JetBrains AI
- Amazon Q Developer
- Cline / Roo Code
- Kiro
- Zed
- Replit
- Aider / OpenCode

## Why This Order

Claude Code and Codex are the priority for ForgeLoop.

Cursor and GitHub Copilot are included because they are common enough that open source users will expect basic support.

The coming-soon tools are visible in the menu so users know the roadmap without ForgeLoop pretending untested integrations are production-ready.

## Sources

- State of Code 2025 results: https://www.stateofcode.ai/2025/survey/result
- SonarSource State of Code Developer Survey 2026: https://www.sonarsource.com/state-of-code-developer-survey-report.pdf
- JetBrains Developer Ecosystem 2025: https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/
- Agentic Much? Adoption of Coding Agents on GitHub: https://arxiv.org/abs/2601.18341
- GitHub Copilot custom instructions: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
