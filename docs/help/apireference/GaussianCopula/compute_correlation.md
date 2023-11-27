---
layout: default
title: Compute Correlation
parent: Gaussian Copula
grand_parent: API Reference
nav_order: 2
---

# GaussianCopula.compute_correlation

Computes the (pairwise) correlation matrix for a given set of data. 
The method used to compute the correlation can be chosen from the available options (kendall, spearman, pearson).

**GaussianCopula.compute_correlation(*data*, [*method*, *transform_to_normal*])**

**Parameters**
- *data*: (dataframe)
  - dataframe that contains the two columns
- *method*: (str)
  - method used to compute the correlation. Available options are 'kendall' (default), 'spearman', and 'pearson'.
- *transform_to_normal*: (bool)
  - If `True`, the data is first transformed to a normal distribution before computing the correlation.

**Returns**
- pandas.DataFrame
  - A square DataFrame with the variable names as indexes and columns, and the correlations as values. 

### Notes

### Examples
```
var1 = np.random.randint(low=1, high=100, size=10)
var2 = np.random.randint(low=1, high=100, size=10)
var3 = np.random.randint(low=1, high=100, size=10)
data = pd.DataFrame({'var1': var1, 'var2': var2, 'var3': var3})
method = 'spearman'
transform_to_normal = True

corr_matrix_df = compute_correlation(data, method, transform_to_normal)
print(corr_matrix_df)

        var1      var2      var3
var1  1.000000  0.774597  0.548821
var2  0.774597  1.000000  0.970860
var3  0.548821  0.970860  1.000000
```