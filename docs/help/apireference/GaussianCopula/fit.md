---
layout: default
title: Fit
parent: Gaussian Copula
grand_parent: API Reference
nav_order: 3
---

# GaussianCopula.fit
Fit the data with a Gaussian copula, i.e.: 
compute the univariate distribution for each variable and then its covariance matrix.

**GaussianCopula.fit(*data*, [*marginal_dist_dict*, ])**

**Parameters**
- *data*: (dataframe)
  - dataframe that contains the two columns
- *marginal_dist_dict*: (dict)
  - A dictionary where keys are variable names and values are lists of candidate marginal distributions. Defaults to `None`.

**Returns**
None. Updates attributes `GaussianCopula.correlation`, `GaussianCopula.univariates`.

### Notes

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [GaussianCopula](../../../gettingStarted/examples/GaussianCopula) | Demonstrates use of GaussianCopula to create multivariate synthetic data. |