# Agent roles

Every topic page goes through three roles, each played by a different session
([10 §10.1–§10.3](../plan/10-ai-agents.md)). Each role's prompt lives in one place only, the
Claude Code skill that runs it. Without Claude Code, read the skill file as the prompt.

| Role | Run | Prompt (the single source) |
|---|---|---|
| Author | `/new-topic <label>` | [`.claude/skills/new-topic/SKILL.md`](../../.claude/skills/new-topic/SKILL.md) |
| Verifier | `/verify-topic <path>` | [`.claude/skills/verify-topic/SKILL.md`](../../.claude/skills/verify-topic/SKILL.md) |
| Reviewer | `/review-math <path>` | [`.claude/skills/review-math/SKILL.md`](../../.claude/skills/review-math/SKILL.md) |
| Second pass (Verifier and Reviewer again) | `/recheck-topic <path>` | [`.claude/skills/recheck-topic/SKILL.md`](../../.claude/skills/recheck-topic/SKILL.md) |

- The conventions every role follows are in [`CLAUDE.md`](../../CLAUDE.md), including the
  owner's sign-off steps.
- The quality bar is the exemplar
  [`content/calculus/limits/limit-of-a-function.md`](../../content/calculus/limits/limit-of-a-function.md),
  judged by the rubric in [`docs/exemplar-review.md`](../exemplar-review.md).
- The PR description template is [`.github/pull_request_template.md`](../../.github/pull_request_template.md).
- `/new-topic` runs [`scripts/new_topic.py`](../../scripts/new_topic.py), which can also be run by hand.
- Cloud sessions are set up by the SessionStart hook,
  [`.claude/hooks/session-start.sh`](../../.claude/hooks/session-start.sh).
