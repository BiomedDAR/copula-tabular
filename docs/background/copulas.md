---
layout: default
title: Copulas
parent: Background
nav_order: 1
math: katex
---

# Overview

Type Maths TEST 3

$$x$$ math at the start of a line

Nested: $$M = \text{while $e^2$ do $c^2$ end}$$

**Numbered equations**

Automatic equation numbering is supported by KaTeX.

$$
\begin{equation}
\int_0^x \sin(x) dx
\end{equation}
$$

`\label` and `\eqref` are not yet implemented.
Using manual tags and HTML links:

$$
\begin{equation}
\int_0^x \sin(x) dx
\htmlId{eq:test}{\tag{1}}
\end{equation}
$$

Link to equation $$\href{#eq:test}{(1)}$$