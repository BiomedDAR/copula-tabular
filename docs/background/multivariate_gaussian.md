---
layout: default
title: Multivariate Gaussian Distribution
parent: Background
nav_order: 3
math: katex
---

## Conditional Multivariate Gaussian Distribution
Consider a multivariate random vector $$X\in\mathbb{R}^{d\times n}$$, $$X\sim\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$$. We want to compute the conditional joint distribution of $$X_1$$ given $$X_2=x_2$$, such that $$X_1\in\mathbb{R}^{d_1\times n}$$, $$X_2\in\mathbb{R}^{d_2\times n}$$, and $$d=d_1+d_2$$. 

We first partition all relevant matrices as follows:
$$
\begin{equation}
\mathbf{X} = 
\end{equation}
$$

$$
\begin{equation}
\mathbf{X} = \begin{bmatrix}
        \mathbf{X_1}\\\mathbf{X_2}
    \end{bmatrix},
    \bm{\mu} = 
    \begin{bmatrix}
        \bm{\mu_1}\\\bm{\mu_2}
    \end{bmatrix},
    \boldsymbol{\Sigma} = 
    \begin{bmatrix}
        \boldsymbol{\Sigma_{11}} & \boldsymbol{\Sigma_{12}} \\
        \boldsymbol{\Sigma_{21}} & \boldsymbol{\Sigma_{22}} &
    \end{bmatrix},
\end{equation}
$$