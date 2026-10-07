---
title: Errata
label: site-errata
description: >-
  How to report an error, how corrections are made, and the public log of mathematical errors
  corrected in verified pages.
maths:
  kind: meta
  status: draft
---

Finding and fixing errors is part of making a reliable reference. This page explains how to
report an error and how we handle it, and it lists every mathematical error that we have
corrected in a verified page.

## Reporting an error

Use **Report an error** at the top of any page. It opens an issue on GitHub. Please tell us:

- the address of the page, and the label of the definition, theorem, example or exercise if
  you know it (it is the part of the address after `#`);
- the kind of problem: a mathematical error, something unclear or misleading, a typo or
  formatting problem, or a broken interactive figure or link;
- what is wrong and, if you can, the correction you suggest;
- how you found it, if you like. This helps us write a test that would have caught it.

## What happens next

1. **Triage**, usually within a week: we confirm the error and label it by severity, or close
   the report with an explanation.
2. **Fix**: for an error in a computation, we first add an automated test that fails on the
   current page, then correct the page so that the test passes.
3. **Log**: if the error was in the mathematics of a verified page, the correction is added
   to the log below, with the date, the page, the label, what was wrong, what changed and a
   link to the report.
4. **Learn**: we ask why our checks missed the error, and improve them if they could have
   caught it.

While a confirmed mathematical error in a verified page is waiting to be fixed, the page
shows a "Known issue" note that links to the report.

## Log of corrections

No corrections have been logged yet.
