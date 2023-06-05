---
layout: default
title: Multivariate Gaussian Distribution
parent: Background
nav_order: 3
math: katex
---

## Conditional Multivariate Gaussian Distribution
Consider a multivariate random vector $$\mathbf{X}\in\mathbb{R}^{d\times n}$$, $$\mathbf{X}\sim\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$$. We want to compute the conditional joint distribution of $$\mathbf{X_1}$$ given $$\mathbf{X_2}=\mathbf{x}_2$$, such that $$\mathbf{X_1}\in\mathbb{R}^{d_1\times n}$$, $$\mathbf{X_2}\in\mathbb{R}^{d_2\times n}$$, and $$d=d_1+d_2$$. 

We first partition all relevant matrices as follows:

$$
\begin{align}
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
\htmlId{eq:test}{\tag{1}}
\end{align}
$$

where $$\boldsymbol{\Sigma_{11}} \in \mathbb{R}^{d_1\times d_1}$$, $$\boldsymbol{\Sigma_{22}} \in \mathbb{R}^{d_2\times d_2}$$, and  $$\boldsymbol{\Sigma_{21}} = \boldsymbol{\Sigma_{12}}^T \in \mathbb{R}^{d_2\times d_1}$$.

The distribution of $$\mathbf{X_1}$$ conditional on $$\mathbf{X_2}=\mathbf{x}_2$$ is a multivariate normal $$(\mathbf{X_1}\mid\mathbf{X_2=\mathbf{x}_2})\sim \mathcal{N}(\bar{\bm{\mu}},\bar{\boldsymbol{\Sigma}})$$, where

$$
\begin{align*}
    \bar{\bm{\mu}} &= \bm{\mu_1} + \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}(\mathbf{x_2}-\bm{\mu_2})\\
    \bar{\boldsymbol{\Sigma}} &= \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}\boldsymbol{\Sigma}_{21}
\end{align*}
$$

We can show this using a trick by creating some linear combination, $$\mathbf{Z}$$, using $$\mathbf{X_1}$$ and $$\mathbf{X_2}$$, such that $$\mathbf{Z}$$ has zero correlation with $$\mathbf{X_2}$$. Since any linear combination of normally distributed random variables is also normally distributed, $$\mathbf{Z}$$ and $$\mathbf{X_2}$$ have a joint normal distribution, and will therefore be independent. This gives us the following expressions:

$$
\begin{align*}
    \mathbf{Z} &= c_1\mathbf{X_1} + c_2\mathbf{X_2} \\
    \text{cov}(\mathbf{Z}, \mathbf{X_2}) &= 0 \\
    \text{var}(\mathbf{Z}\mid\mathbf{X_2}) &= \text{var}(\mathbf{Z})\\
    \mathbb{E}(\mathbf{Z}\mid\mathbf{X_2}) &= \mathbb{E}(\mathbf{Z}) = c_1\bm{\mu_1} + c_2\bm{\mu_2}
\end{align*}
$$

We have

$$
\begin{align*}
    \mathbb{E}(\mathbf{Z}\mid\mathbf{X_2}) = \mathbb{E}(c_1\mathbf{X_1} + c_2\mathbf{X_2} \mid \mathbf{X_2}) &= c_1\bm{\mu_1} + c_2\bm{\mu_2}\\
    c_1\mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) + c_2\mathbf{X_2} &= c_1\bm{\mu_1} + c_2\bm{\mu_2}\\
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + \frac{c_2}{c_1}( \bm{\mu_2} - \mathbf{X_2} ) \\
\end{align*}
$$

Let $$A:=\frac{c_2}{c_1}$$. Then

$$
\begin{align*}
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + A ( \bm{\mu_2} - \mathbf{X_2} ) \\
\end{align*}
$$

Then

$$
\begin{align*}
    \text{var}(\mathbf{X_1}\mid\mathbf{X_2}) &= \text{var}\bigg(\frac{1}{c_1}(\mathbf{Z}-c_2\mathbf{X_2})\mid\mathbf{X_2} \bigg)\\
    &=\text{var}\bigg(\frac{1}{c_1}(\mathbf{Z})\mid\mathbf{X_2} \bigg)\\
    &= \text{var}\bigg(\frac{1}{c_1}(\mathbf{Z}) \bigg)\\
    &= \text{var}\bigg(\mathbf{X_1} + A(\mathbf{X_2}) \bigg)\\
    &= \text{var}(\mathbf{X_1}) + A\text{var}(\mathbf{X_2})A^T + A\text{cov}(\mathbf{X_1},\mathbf{X_2}) + \text{cov}(\mathbf{X_2},\mathbf{X_1})A^T \\
    &= \boldsymbol{\Sigma}_{11} + A\boldsymbol{\Sigma}_{22}A^T + A\boldsymbol{\Sigma}_{12} + \boldsymbol{\Sigma}_{21}A^T\\
    &= \boldsymbol{\Sigma}_{11} + A\boldsymbol{\Sigma}_{22}A^T + 2A\boldsymbol{\Sigma}_{12} \\
    &=\boldsymbol{\Sigma}_{11} + A ( \boldsymbol{\Sigma}_{22}A^T + 2\boldsymbol{\Sigma}_{12}  )
\end{align*}
$$

We are left with the problem of determining $$A$$.
Using

$$
\begin{align*}
    \text{cov}(\mathbf{Z}, \mathbf{X_2}) = c_1\text{cov}(\mathbf{X_1}, \mathbf{X_2}) + c_2 \text{cov}(\mathbf{X_2}, \mathbf{X_2})&=0\\
    c_1\text{cov}(\mathbf{X_1}, \mathbf{X_2}) + c_2 \text{var}(\mathbf{X_2}) &= 0\\
    \text{cov}(\mathbf{X_1}, \mathbf{X_2}) &= - \frac{c_2}{c_1} \text{var}(\mathbf{X_2})\\
    \boldsymbol{\Sigma_{12}} &= - A \boldsymbol{\Sigma_{22}}\\
    A &= -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1}\\
\end{align*}
$$

This gives us the expressions for mean and covariance respectively as follows:

$$
\begin{align*}
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + \boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( \mathbf{X_2} - \bm{\mu_2}) \\
\end{align*}
$$

$$
\begin{align*}
    \text{var}(\mathbf{X_1}\mid\mathbf{X_2}) &= \boldsymbol{\Sigma}_{11} + A ( \boldsymbol{\Sigma}_{22}A^T + 2\boldsymbol{\Sigma}_{12}  )\\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( -\boldsymbol{\Sigma}_{22}\boldsymbol{\Sigma_{22}}^{-1}\boldsymbol{\Sigma_{21}} + 2\boldsymbol{\Sigma}_{12} ) \\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( -\boldsymbol{\Sigma_{21}} + 2\boldsymbol{\Sigma}_{12} ) \\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1}\boldsymbol{\Sigma_{21}} \\
\end{align*}