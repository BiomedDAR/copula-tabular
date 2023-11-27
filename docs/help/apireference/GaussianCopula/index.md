---
layout: default
title: Gaussian Copula
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# GaussianCopula

`class GaussianCopula(debug=False, correlation_method="kendall")`
Learn/Build Gaussian Copula for multivariate data.

### Parameters

**debug**: boolean, default `False`. Whether to print debug-related outputs to console.

**correlation_method**: str, default `kendall`. Method for computing covariance matrix

### Notes

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [GaussianCopula](../../../gettingStarted/examples/GaussianCopula) | Demonstrates use of GaussianCopula to create multivariate synthetic data. |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug | (boolean) whether to debug or not  |
| var_names | (list) array of column names found in data dataframe |
| univariates | (dict) dictionary where the key is the variable name and the value is the fitted MarginalDist instances |
| correlation | (array) computed correlation matrix |
| fitted | (boolean) whether copula has been fitted |

### Methods

| Method         | Description | 
| ---:              |    :----   |
| print_copula_params() | Display copula parameters |
| compute_correlation(data, [method, transform_to_normal]) | Compute the (pairwise) correlation matrix using input data method. Default: "kendall", options include "kendall", "spearman", "pearson". |
| fit(data, [marginal_dist_dict, ]) | Compute the distribution for each variable and then its covariance matrix | 
| conditional_Gaussian(conditions) | Compute the parameters (mean, covariance) of a conditional multivariate normal distribution. (`conditions` is a `pandas.series` variable) |
| sample([size, conditions]) | Generates synthetic data from a fitted Gaussian Copula Model |