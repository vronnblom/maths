---
title: Content Status
label: site-status
description: >-
  What the statuses draft, reviewed and verified mean, which checks a page passes to reach
  each one, and how far the pages have got.
maths:
  kind: meta
  status: draft
---

Every page is published as soon as it is written, so that readers can use it and report
errors early. Each page shows its **status**, so you always know how far it has been checked.

## What the statuses mean

| Status | What it means | Checks that a page has passed |
|---|---|---|
| **Draft** | Written, but not yet checked. It may contain errors. | The site builds, and the page's metadata is valid. |
| **Reviewed** | The mathematics has been read and approved by the maintainer. | Every proof has been checked against a written checklist, and at least half of the worked examples and exercises have a computer check that passes. Every page it builds on is at least reviewed. |
| **Verified** | Every computation has been checked by a computer, and the proofs have been reviewed twice. | Every worked example and every exercise answer is checked by the computer algebra system SymPy, or, for a proof, by a person. The proofs have been checked by the maintainer and by a second reviewer. No proof relies on a result that comes later. Every page it builds on is at least reviewed. |

A draft page carries a banner warning that it may contain errors.

## Keeping verified pages verified

Any change to the mathematics of a verified page (a statement, a proof, an example or an
answer) has to pass the same checks again; otherwise the page goes back to reviewed.
Corrections of mathematical errors in verified pages are logged publicly on the
[errata page](#site-errata).

## Pages by status

The tables below are generated from the curriculum and the pages themselves each time the site
is built, so they always match the published pages. A planned topic is one that is in the
curriculum but not written yet.

% Written by scripts/generate.py before every build; never edit or commit it.
```{include} _generated/status-table.md
```
