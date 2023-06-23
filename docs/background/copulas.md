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

## Density of a Copula
If the multivariate distribution has a density, $$h(x_1, \dots, x_d)$$, we can then get a closed formed formula for copula density $$c(F_{X_1}(x_1), \dots, F_{X_d}(x_d))$$. Using the definition of $$h(x_1, \dots, x_d)$$, we have

$$
\begin{align*}
    h(x_1, \dots, x_d) &= \frac{\partial^d H(x_1, \dots, x_d)}{\partial x_1 \dots \partial x_d} \\
    &= \frac{\partial^d C(F_{X_1}(x_1), \dots, F_{X_d}(x_d))}{\partial x_1 \dots \partial x_d} \\
    &= \frac{\partial^d C(F_{X_1}(x_1), \dots, F_{X_d}(x_d))}{\partial F_{X_1}(x_1) \dots \partial F_{X_d}(x_d)} 
    \prod^d_{i=1} \frac{\partial F_{X_i}(x_i)}{\partial x_i}  \\
    &= c(F_{X_1}(x_1), \dots, F_{X_d}(x_d)) \prod^d_{i=1} f_{X_i}(x_i)\\ 
\end{align*}
$$

## Conditional Copula
Given a three dimensional vector $$(X_1, X_2, Y)$$, we study the *dependence structure* of $$(X_1, X_2)$$ for a given value of $$(Y=y)$$.

Let

$$
\begin{equation}
H_y(x_1, x_2) := \mathbb{P} (X_1 \leq x_1, X_2 \leq x_2 \vert Y=y)
% \htmlId{eq:test}{\tag{1}}
\end{equation}
$$

According to the Sklar's Theorem, there exists a *conditional copula function* $$C_y$$ such that

$$
\begin{equation}
H_y(x_1, x_2) = C_y(F_{1y}(x_1), F_{2y}(x_2)),
% \htmlId{eq:conditional_copula_function}{\tag{2}}
\end{equation}
$$

where $$F_{1y}$$ and $$F_{2y}$$ are the corresponding conditional marginals of $$X_1$$ and $$X_2$$ respectively.

## Partial Copula
Let $$U_1:= F_{1y}(X_1)$$, $$U_2:= F_{2y}(X_2)$$. The *partial copula function* is defined as

$$
\begin{align*}
\bar{C}(u_1, u_2) &:= \mathbb{P} (U_1 \leq u_1, U_2 \leq u_2) \\
&= \int \mathbb{P} (U_1 \leq u_1, U_2 \leq u_2 \vert X=x) f_Y(y) dy \\
&= \int C_x(u_1, u_2) f_Y(y) dy
% \htmlId{eq:partial_copula_function}{\tag{3}}
\end{align*}
$$


<!-- Link to equation $$\href{#eq:test}{(1)}$$ -->