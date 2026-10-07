# Architecture decision records

Architecture decisions (tooling, schema, label grammar, licences, the CI gates) are recorded
here as short ADRs, so the plan doesn't drift without anyone noticing ([11 §11.3](../plan/11-governance.md)).
Curriculum changes are not ADRs: they go through a `curriculum` PR.

## ADR 0000: the plan

The plan documents in [`docs/plan/`](../plan/) (01–12) and [`PLAN.md`](../../PLAN.md) are
ADR 0000: every decision made before the first ADR, with its reasons and the options it
rejected. They keep being corrected when an implementation stage proves them wrong; each
correction is named in its PR.

## Writing an ADR

A decision that changes something ADR 0000 settled gets its own file,
`docs/decisions/NNNN-short-title.md` (the next free number, four digits, kebab-case), added in
the PR that makes the change, and approved by the maintainer like the change itself:

```markdown
# NNNN. Short title

Status: accepted | superseded by NNNN · Date: YYYY-MM-DD · PR: #123

## Context

What forces the decision: the problem, the constraints, what changed since the plan.

## Decision

What we do, stated so that someone could check whether the repository follows it.

## Consequences

What becomes easier and what becomes harder; what else must change (plan sections, CLAUDE.md,
checks); what would make us revisit it.
```

The PR also updates the plan section it supersedes, with a link to the ADR, so that
`docs/plan/` stays the readable description of the repository as it is. An ADR is never
edited after it is accepted, except to mark it superseded.

## Index

| ADR | Title | Status |
|---|---|---|
| 0000 | [The plan](../plan/) | accepted |
