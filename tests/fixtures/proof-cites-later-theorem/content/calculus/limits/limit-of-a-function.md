---
title: The Limit of a Function
label: calc-limit
description: A fixture page.
maths:
  kind: topic
  subject: calc
  status: verified
  level: core
  difficulty: 2
  est_minutes: 30
  prerequisites: []
  objectives:
    - State the definition.
    - Compute an example.
  verify: verify/calculus/limits/test_limit_of_a_function.py
  reviewed_by: [vronnblom]
---

## What a limit is

:::{proof:definition} Limit of a function
:label: def-calc-limit
We say that **the limit of $f(x)$ as $x$ approaches $a$ is $L$** if …
:::

## Main results

:::{proof:theorem} Uniqueness of limits
:label: thm-calc-limit-unique
If $\lim_{x\to a} f(x) = L$ and $\lim_{x\to a} f(x) = M$, then $L = M$.
:::

:::{proof:theorem} Limits are local
:label: thm-calc-limit-local
If $f = g$ near $a$ (except possibly at $a$), then $f$ and $g$ have the same limits at $a$.
:::

:::{proof:proof}
:enumerated: false
Both conditions in [](#def-calc-limit) only involve $x$ with $0 < \abs{x - a} < \delta$.
:::

## Rigorous track

:::{proof:proof} Rigorous track
:label: prf-calc-limit-unique
:enumerated: false
:class: dropdown
We prove [](#thm-calc-limit-unique). By [](#thm-calc-limit-local) we may change $f$ at $a$ … Suppose $L \ne M$ …
:::
