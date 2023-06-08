---
layout: default
title: Multivariate Gaussian Distribution
parent: Background
nav_order: 3
math: katex
---

# Multivariate Gaussian Distributions

## As a member of an Elliptical-Contoured Distribution
For details, please refer to [Fang et al.](https://www.sciencedirect.com/science/article/pii/S0047259X01920172?ref=pdf_download&fr=RR-2&rr=7d05d3866a259fb6)

Let $$Z$$ be a $$d$$-dimensional random vector that follows a stochastic representation $$\bm{\mu} + r\mathbf{A}\mathbf{u}$$
such that
*   $$\bm{\mu} \in \mathbb{R}^{d\times 1}$$ (location vector)
*   $$r \geq 0$$, $$r$$ is a (univariate) random variable of some density (independent radial part)
*   $$\mathbf{A}\mathbf{A}^T = \boldsymbol{\Sigma}, \boldsymbol{\Sigma}\in\mathbb{R}^{d\times d}$$ (positive-definite matrix modelling the covariance)
*   $$\mathbf{u}$$ is uniformly distributed on the unit sphere in $$\mathbb{R}^d, i.e. \mathbf{u}\sim U(\{ \mathbf{x} \in \mathbb{R}^d: \lVert \mathbf{x} \rVert=1 \})$$

One can think of $$\mathbf{A}$$, the Cholesky factor of some covariance matrix, as some multivariate linear transformation acting on $$r\mathbf{u}$$, a spherical distribution.

The probability density of $$Z \sim \text{EC}_d(\bm{\mu}, \boldsymbol{\Sigma}, g)$$ can be written in the form

$$
\begin{align}
    \lvert \boldsymbol{\Sigma} \rvert^{-1/2} g( (Z-\bm{\mu})^T \boldsymbol{\Sigma}^{-1} (Z-\bm{\mu}) ),
\end{align}
$$

where $$g(\cdot)$$ is some scale function uniquely determined by the distribution of $$r$$.

When

$$
\begin{align}
    g(x) := \frac{1}{(2\pi)^{d/2}} \exp (\frac{-x}{2}), 
\end{align}
$$

$$Z$$ has a $$d$$-dimensional Gaussian probability distribution (also denoted as $$\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$$):

$$
\begin{align}
    \frac{1}{ ((2\pi)^{d} \lvert \boldsymbol{\Sigma} \rvert)^{1/2} } \exp \bigg(\frac{-1}{2} (Z-\bm{\mu})^T \boldsymbol{\Sigma}^{-1} (Z-\bm{\mu}) \bigg)
\end{align}
$$

where $$\boldsymbol{\Sigma}: \{ \rho_{ij} \}$$ is some postive definite (correlation matrix) such that for $$i,j = 1,\dots, d$$, $$\rho_{ij} = \rho_{ji}$$, and

$$
\begin{align}
    \rho_{ij} =  \begin{cases}
        1 &\text{ if } i=j,\\
        0 < \rho_{ij} < 1 &\text{ if } i\neq j
    \end{cases}
\end{align}
$$

## Conditional Multivariate Gaussian Distribution
Consider a multivariate random vector $$\mathbf{X}\in\mathbb{R}^{d\times n}$$, $$\mathbf{X}\sim\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$$. We want to compute the conditional joint distribution of $$\mathbf{X_1}$$ given $$\mathbf{X_2}=\mathbf{x}_2$$, such that $$\mathbf{X_1}\in\mathbb{R}^{d_1\times n}$$, $$\mathbf{X_2}\in\mathbb{R}^{d_2\times n}$$, and $$d=d_1+d_2$$. 

We first partition all relevant matrices as follows:

$$
\begin{align*}
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
\end{align*}
$$

where $$\boldsymbol{\Sigma_{11}} \in \mathbb{R}^{d_1\times d_1}$$, $$\boldsymbol{\Sigma_{22}} \in \mathbb{R}^{d_2\times d_2}$$, and  $$\boldsymbol{\Sigma_{21}} = \boldsymbol{\Sigma_{12}}^T \in \mathbb{R}^{d_2\times d_1}$$.

The distribution of $$\mathbf{X_1}$$ conditional on $$\mathbf{X_2}=\mathbf{x}_2$$ is a multivariate normal $$(\mathbf{X_1}\mid\mathbf{X_2=\mathbf{x}_2})\sim \mathcal{N}(\bar{\bm{\mu}},\bar{\boldsymbol{\Sigma}})$$, where

$$
\begin{align*}
    \bar{\bm{\mu}} &= \bm{\mu_1} + \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}(\mathbf{x_2}-\bm{\mu_2})\\
    \bar{\boldsymbol{\Sigma}} &= \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}\boldsymbol{\Sigma}_{21}
\end{align*}
$$

<!-- <details>
    <summary>Proof</summary> -->
### Proof
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
    c_1\mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) + c_2\mathbf{x_2} &= c_1\bm{\mu_1} + c_2\bm{\mu_2}\\
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + \frac{c_2}{c_1}( \bm{\mu_2} - \mathbf{x_2} ) \\
\end{align*}
$$

Let $$A:=\frac{c_2}{c_1}$$. Then

$$
\begin{align*}
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + A ( \bm{\mu_2} - \mathbf{x_2} ) \\
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
    &= \boldsymbol{\Sigma}_{11} + A\boldsymbol{\Sigma}_{22}A^T + A\boldsymbol{\Sigma}_{21} + \boldsymbol{\Sigma}_{12}A^T\\
    &= \boldsymbol{\Sigma}_{11} + A\boldsymbol{\Sigma}_{22}A^T + 2A\boldsymbol{\Sigma}_{21} \\
    &=\boldsymbol{\Sigma}_{11} + A ( \boldsymbol{\Sigma}_{22}A^T + 2\boldsymbol{\Sigma}_{21}  )
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
    \mathbb{E}(\mathbf{X_1} \mid \mathbf{X_2} ) &= \bm{\mu_1} + \boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( \mathbf{x_2} - \bm{\mu_2}) \\
\end{align*}
$$

$$
\begin{align*}
    \text{var}(\mathbf{X_1}\mid\mathbf{X_2}) &= \boldsymbol{\Sigma}_{11} + A ( \boldsymbol{\Sigma}_{22}A^T + 2\boldsymbol{\Sigma}_{21}  )\\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( -\boldsymbol{\Sigma}_{22}\boldsymbol{\Sigma_{22}}^{-1}\boldsymbol{\Sigma_{21}} + 2\boldsymbol{\Sigma}_{21} ) \\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1} ( -\boldsymbol{\Sigma_{21}} + 2\boldsymbol{\Sigma}_{21} ) \\
    &= \boldsymbol{\Sigma}_{11} -\boldsymbol{\Sigma_{12}}\boldsymbol{\Sigma_{22}}^{-1}\boldsymbol{\Sigma_{21}} \\
\end{align*}
$$

<!-- </details> -->

## Copulas from Meta-Elliptical Distributions
Let $$\mathbf{X} = (X_1, X_2, \dots, X_d)^T$$ be a random vector with each component $$X_i$$ having a given continuous marginal probability density $$f_i(x_i)$$ and corresponding cumulative distribution $$F_i(x_i)$$. Without loss of generality, let $$Z:=(Z_1, Z_2, \dots, Z_d)^T \sim \text{EC}_d(\bm{0}, \boldsymbol{\Sigma}, g)$$ where $$g$$ is given by

$$
\begin{align}
    g(x) := \frac{1}{(2\pi)^{d/2}} \exp (\frac{-x}{2}).
\end{align}
$$

Then

$$
\begin{align}
    Z_i = Q_g^{-1}( F_i(X_i) ),
\end{align}
$$

where $$Q_g^{-1}$$ is the inverse of $$Q_g$$, a univariate standard Gaussian distribution $$\mathcal{N}(0,1)$$.

$$\mathbf{X}$$ is said to have a *meta-elliptical distribution*.
The density function of $$\mathbf{X}$$ is then

$$
\begin{align}
    h(x_1, x_2, \cdots, x_d) = \phi(Q_g^{-1}( F_1(X_1) ), Q_g^{-1}( F_2(X_2) ), \dots, Q_g^{-1}( F_d(X_d) ) ) \prod^d_{i=1} f_x(x_i),
\end{align}
$$

where $$\phi$$ is the $$d$$-dimensional multivariate weighted Gaussian density function.