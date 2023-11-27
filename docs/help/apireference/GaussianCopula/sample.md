---
layout: default
title: Sample
parent: Gaussian Copula
grand_parent: API Reference
nav_order: 4
---

# GaussianCopula.sample
Generates synthetic data from a fitted Gaussian Copula Model.

**GaussianCopula.sample([*size*, *conditions*])**

**Parameters**
- *size*: (int)
  - number of synthetic samples to generate. If not specified, default is `1`.
- *conditions*: (dict)
  - A dictionary containing values for conditional variables in the form of `{variable_name: value}`. If no conditions are specified, the full joint Gaussian distribution will be used.

**Returns**
- pandas.DataFrame
  - A dataframe containing the synthetic samples.

### Notes

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [GaussianCopula](../../../gettingStarted/examples/GaussianCopula) | Demonstrates use of GaussianCopula to create multivariate synthetic data. |