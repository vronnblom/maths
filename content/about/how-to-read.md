---
title: How to Read This Site
short_title: How to read this site
label: site-how-to-read
description: >-
  How the pages are organised: the core text and the rigorous track, proofs, worked examples,
  exercise tiers, links with previews, and what a page's status means.
maths:
  kind: meta
  status: draft
---

## Subjects, chapters and topics

The site is organised as **subject → chapter → topic**. A topic page is the unit you read in
one sitting, typically 20 to 45 minutes. Each topic lists the topics you should know first
("Before you start") and the topics that build on it ("Where this leads"), so you can move
backwards to fill a gap or forwards to see where an idea is used.

Every topic page has the same sections, in the same order:

1. **Why this matters**: the question the topic answers, with a concrete example.
2. **Definitions** and **results**: the precise statements, each followed by an explanation
   in words and examples.
3. **Worked examples**: complete solutions with every step shown, each ending with a check.
4. **Common mistakes**: errors that students often make, why they are wrong, and how to fix
   them.
5. **Rigorous track** (on some pages): proofs and subtleties for readers who want full rigour.
6. **Summary**: the key points and formulas.
7. **Exercises**: tiered practice with hints, answers and full solutions.
8. **Where this leads**: the topics that build on this one.

## The core text and the rigorous track

The **core text** is written for a first-year student of engineering or science. It gives the
motivation, the definitions, the statements of the results, the proofs that build
understanding, and plenty of worked examples.

The **rigorous track** is for readers who want every detail, for example mathematics majors.
It appears as collapsed blocks marked "Rigorous track". You can skip all of them on a first
reading and still follow the core text. Open them when you want to see why a result is true
in full detail.

Each result is handled in one of four ways:

| You see | Meaning |
|---|---|
| **Proof** | a full proof in the core text |
| **Proof (Rigorous track)** | a full proof, collapsed; open it if you want it |
| **Proof (Sketch)** | the main idea of the proof; the text says what is left out |
| a link to another page | the proof needs tools from elsewhere, and the page names where it is proved |

## Numbers and links

Definitions, theorems, examples and exercises are numbered separately on each page, and the
numbers start again on every page. A link to a block on another page is therefore always
named ("the squeeze theorem"), never just "Theorem 2".

Hover over a link (or tap it on a phone) to preview what it points to without leaving the
page. Every block has a permanent address, so a link to a theorem keeps working even if the
pages around it are reorganised.

## Exercises

Exercises come in three tiers:

| Tier | Name | What it asks |
|---|---|---|
| A | Check | a direct application of one definition or rule; a few minutes |
| B | Practice | several steps, combining two or three ideas, and choosing an approach |
| C | Challenge | proofs, the reason a hypothesis is needed, or a new application |

Some exercises carry an extra tag. **Rigorous** means the exercise needs the rigorous track,
so you can skip it if you are not following that track. **Applied** means the exercise comes
from a modelling, physics or economics context.

Each exercise has, separately collapsed, one or more **hints**, the final **answer**, and a
full **solution**. Try the exercise first. If you are stuck, open one hint at a time. Check
your answer, and read the solution even when your answer is right: it may show a shorter
route.

## Interactive figures

Some figures are interactive: you can move sliders, zoom, and read off values. Each one
comes with a **Try this** prompt saying what to change and what to notice, and a caption
describing what it shows, so the content is also available without the interaction (for
example when JavaScript is off). The sliders and buttons work with the keyboard: press Tab to
reach one, then use the arrow keys (or Home and End) to move a slider. Here is one:

::::{figure}
:label: wdg-site-transformed-sine

```{anywidget} ../../widgets/function-plot.mjs
{
  "f": "a*sin(b*(x - c)) + d",
  "xRange": [-6.5, 6.5],
  "yRange": [-4, 4],
  "parameters": {
    "a": { "value": 1, "min": -2, "max": 2, "step": 0.5 },
    "b": { "value": 1, "min": 0.5, "max": 3, "step": 0.5 },
    "c": { "value": 0, "min": -3, "max": 3, "step": 0.5 },
    "d": { "value": 0, "min": -1.5, "max": 1.5, "step": 0.5 }
  },
  "table": { "points": [0, 0.5, 1, 1.5, 2] }
}
```

Graph of $y = a \sin(b(x - c)) + d$ for $-6.5 \le x \le 6.5$, with a slider for each of $a$,
$b$, $c$ and $d$, and a table of values at $x = 0, 0.5, 1, 1.5, 2$. At first
$a = b = 1$ and $c = d = 0$, which gives $y = \sin x$. Changing $a$ stretches the graph
vertically, $b$ squeezes it horizontally, $c$ shifts it to the right and $d$ shifts it up.
::::

**Try this:** set $b = 2$. How far apart are the peaks now? Then make $a$ negative: what
happens to the graph, and to the values in the table?

## Page status

Every page shows how far it has got through our quality checks:

| Status | Meaning |
|---|---|
| **Draft** | written, but not yet checked; it may contain errors |
| **Reviewed** | the mathematics has been read and approved by the maintainer |
| **Verified** | every computation in the worked examples and every exercise answer has also been checked by a computer algebra system, and the proofs have been reviewed twice |

Pages are published at every status so that they can be read and corrected early. The
[content status](#site-status) page explains the checks in more detail. If you find an error
on any page, please [report it](#site-errata).
