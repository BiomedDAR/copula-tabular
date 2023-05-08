---
layout: default
title: Copulas
parent: Background
nav_order: 1
math: katex
---

# Overview

## Conditional Copula
Given a three dimensional vector $$(Y_1, Y_2, X)$$, we study the *dependence structure* of $$(Y_1, Y_2)$$ for a given value of $$(X=x)$$.

Let

$$
\begin{equation}
H_x(y_1, y_2) := \mathbb{P} (Y_1 \leq y_1, Y_2 \leq y_2 \vert X=x)
\htmlId{eq:test}{\tag{1}}
\end{equation}
$$

According to the Sklar's Theorem, there exists a *conditional copula function* $$C_x$$ such that

$$
\begin{equation}
H_x(y_1, y_2) = C_x(F_{1x}(y_1), F_{2x}(y_2)),
\htmlId{eq:conditional_copula_function}{\tag{2}}
\end{equation}
$$

where $$F_{1x}$$ and $$F_{1x}$$ are the corresponding conditional marginals of $$Y_1$$ and $$Y_2$$ respectively.

## Partial Copula
Let $$U_1:= F_{1x}(Y_1)$$, $$U_1:= F_{2x}(Y_2)$$. The *partial copula function* is defined as

$$
\begin{align*}
\bar{C}(u_1, u_2) &:= \mathbb{P} (U_1 \leq u_1, U_2 \leq u_2) \\
&= \int \mathbb{P} (U_1 \leq u_1, U_2 \leq u_2 \vert X=x) f_X(x) dx \\
&= \int C_x(u_1, u_2) f_X(x) dx
\htmlId{eq:partial_copula_function}{\tag{3}}
\end{align*}
$$


<!-- Link to equation $$\href{#eq:test}{(1)}$$ --> -->