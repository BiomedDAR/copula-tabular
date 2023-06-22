---
layout: default
title: Copulas
parent: Background
nav_order: 1
math: katex
---

# Overview

## What is a Copula?
A ($$d$$-dimensional) copula, $$C: [0,1]^d \rightarrow [0,1]$$, is simply a (joint) cumulative distribution function (CDF) with standard uniform marginal distributions (defined between $$0$$ and $$1$$). Alternatively, we say a function $$C: [0,1]^d \rightarrow [0,1]$$ is a copula if and only if it fulfills all of the following properties:
*   $$C(u_1, \dots, u_d)$$ is non-decreasing in each $$u_i$$, $$i \in \{1,\dots, d\}$$
*   $$C(1,1, \dots, u_i,\dots,1,1) = u_i$$
*   $$\forall a_i\leq b_i, \mathbb{P} (U_1 \in [a_1, b_1], \dots , U_d \in [a_d, b_d]) \leq 0$$ (implies rectangle inequality)

Given a marginal CDF, $$F_X: x\mapsto F_X(x)=u$$, its generalised inverse, $$F_X^{(-1)}$$ is defined as $$F_X^{(-1)}(u) := \inf\{x: F_X(x) \geq u \}$$. Then for $$U\sim U[0,1]$$, we have

$$
\begin{align}
    \mathbb{P} (F_X^{(-1)} (U) \leq x  ) = F_X(x)
\end{align}
$$

When $$F_X$$ is continuous, we also have

$$
\begin{align}
    F_X(X) \sim U[0,1].
\end{align}
$$

We now extend the above into the multivariate scenario where $$\mathbf{X} = (X_1, X_2, \dots, X_d)$$ is a multivariate random vector with joint CDF, $$H$$, with continuous and increasing marginal CDFs, $$F_{X_1} \dots, F_{X_d}$$. We have

$$
\begin{align}
    H(x_1, \dots, x_d) = \mathbb{P} ( X_1 \leq x_1, \dots, X_d \leq x_d )
\end{align}
$$

Since $$F_{X_i}(X_i) \sim U[0,1], \forall i \in \{1,\dots, d\}$$, the joint distribution of $$F_{X_1}(X_1) \dots F_{X_d}(X_d)$$ fulfils the definition of a copula. Using the definition of joint distributions, we have

$$
\begin{align*}
    C(u_1, \dots, u_d) &= \mathbb{P} ( F_{X_1}(X_1)  \leq u_1, \dots, F_{X_d}(X_d) \leq u_d )\\
    &= \mathbb{P} ( X_1 \leq F^{(-1)}_{X_1}(u_1), \dots, X_d \leq F^{(-1)}_{X_d}(u_d) )\\
    &= H(F^{(-1)}_{X_1}(u_1), \dots, F^{(-1)}_{X_d}(u_d))
\end{align*}
$$

Let $$u_i = F_{X_i}(x_i)$$. Then we have

$$
\begin{align}
    C(F_{X_1}(x_1), \dots, F_{X_d}(x_d)) = H(x_1, \dots, x_d),
    \htmlId{eq:copula_function}{\tag{4}}
\end{align}
$$

## Sklar's Theorem and Building Joint Distributions

This gives us first half of the Sklar's Theorem: Given a ($$d$$-dimensional) CDF, $$H$$, with marginals, $$F_{X_1} \dots, F_{X_d}$$, there exists a copula, $$C$$, such that 

$$
\begin{align*}
    C(F_{X_1}(x_1), \dots, F_{X_d}(x_d)) = H(x_1, \dots, x_d).
\end{align*}
$$

When $$F_{X_i}$$ is continuous for all $$i \in \{1,\dots, d\}$$, $$C$$ is unique; otherwise $$C$$ is uniquely determined only on $$\text{Ran}(F_{X_1}) \times \dots \times \text{Ran}(F_{X_d})$$ ($$\text{Ran}(F_{X_i})$$ is the range of $$F_{X_i}$$ ).

Unfortunately, we seldom, if ever, know the joint CDF of a multivariate dataset.
To generate synthetic data, we often use the second half the Sklar's Theorem: Given some copula, $$C$$, and univariate CDFs, $$F_{X_1} \dots, F_{X_d}$$, we can find a unique joint CDF, $$H$$, as defined in equation $$\href{#eq:copula_function}{(4)}$$, with marginals $$F_{X_1} \dots, F_{X_d}$$.

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

where $$F_{1x}$$ and $$F_{2x}$$ are the corresponding conditional marginals of $$Y_1$$ and $$Y_2$$ respectively.

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


<!-- Link to equation $$\href{#eq:test}{(1)}$$ -->