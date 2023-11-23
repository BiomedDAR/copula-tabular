---
layout: default
title: Marginal Distributions
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# MarginalDist

`class MarginalDist(debug=False)`
Learn/Build marginal distributions for univariate data.

### Parameters

**debug**: boolean, default `False`. Whether to print debug-related outputs to console.

### Notes

#### Reference List of Distributions

The following methods are used in the same way:
```
xx_dist(data, operation=<chosen operation>, new_params=<dict of params>, sample_size=<int>)
```

List of operations:
* *fit*: given some input `data`, find the best parameters for chosen xx distribution
* *sample*: given some params (given as `new_params` or from prior fitted distribution), sample some datapoints from chosen xx distribution. Number of datapoints = `sample_size`
* *pdf* : given some params (given as `new_params` or from prior fitted distribution), return the PDF for points given in `data`.
* *cdf* : given some params (given as `new_params` or from prior fitted distribution), return the CDF for points given in `data`.
* *ppf* : given some params (given as `new_params` or from prior fitted distribution), return the PPF for "probability" given in `data`.


| Ref. String         | Method | Parameters |
| ---:              |    :----   | |
| beta | beta_dist | loc, scale, a, b |
| laplace | laplace_dist | loc, scale |
| loglaplace | loglaplace_dist | c, loc, scale |
| gamma | gamma_dist | loc, scale, a |
| gaussian | gaussian_dist | loc, scale |
| student_t | t_dist | loc, scale |
| uniform | uni_dist | loc, scale |
| emp | empirical_dist | loc, scale |
| gaussian_kde | gaussian_kde_dist | scale |
| degenerate | degenerate_dist | constant_value |


### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [Univariate](../../../gettingStarted/examples/Univariate) | Demonstrates use of MarginalDist to create univariate synthetic data. |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug | (boolean) whether to debug or not  |
| marginal_dist | (str) Type of marginal distribution the class instance is set to.  |
| fitted_marginal_dist | (str) Type of marginal distribution the data is fitted to.  |
| sample_size | (int) Number of samples to generate.   |
| gaussian_kde_model | (obj) `stats.gaussian_kde` instance used.   |
| fitted | (boolean) Set to `True` if successfully fitted.  |
| params | (dict) List of parameters for fitted marginal distribution   |
| sample_cdf | () CDF of samples used to fit the distribution   |
| sample_pdf | () PDF of samples used to fit the distribution  |
| samples | ()  x-values (samples) generated based on parameters (fitted or given) |
| cdf | ()  cumulative probability of new data input based on parameters (either fitted or given) |
| pdf | ()  probability of new data input based on parameters (either fitted or given) |
| ppf | ()  x-value of cumulative probability of new data input |
| parametric | ()  List of parametric distributions: `["beta", "laplace", "loglaplace", "gamma", "gaussian", "student_t", "uniform"]` |
| nonparametric | ()  List of non-parametric distributions: `["emp", "gaussian_kde"]` |

### Methods

| Method         | Description | 
| ---:              |    :----   |
| load_params([new_params, ]) | Replace `MarginalDist.params` with specified parameters in `new_params` dictionary. |
| generic_cdf(x, fn_pdf) | Compute generic CDF using integration |
| inv_CDF_fn(x, u) | Build CDF inverse function |
| fwd_CDF_fn(x, u) | Build CDF forward function |
| eCDF_fn(input, x, u, [init_val, ]) | Implements eCDF. For each element in `input`, it finds its best position in `x`, determines the corresponding cumulative probability from `u`, and returns the interpolated cumulative probability. |
| ecdf(x) | Computes the ECDF of `x`. Use only for continuous distributions. |
| beta_dist([data, operation, new_params, sample_size]) | Compute Beta Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| laplace_dist([data, operation, new_params, sample_size]) | Compute Laplace Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| loglaplace_dist([data, operation, new_params, sample_size]) | Compute log Laplace Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| gamma_dist([data, operation, new_params, sample_size]) | Compute Gamma Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| gaussian_dist([data, operation, new_params, sample_size]) | Compute Gaussian Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| t_dist([data, operation, new_params, sample_size]) | Compute Student-t Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| uni_dist([data, operation, new_params, sample_size]) | Compute Uniform Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| degenerate_dist([data, operation, new_params, sample_size]) | Compute Degenerate Distribution related operations, including `fit`, `sample`, `pdf`, `cdf`, `ppf`. |
| gaussian_kde_dist([data, operation, new_params, sample_size, bw_method, weights]) | Compute Gaussian Kernel Density Estimate related operations, including `fit`, `pdf`, `cdf`, `ppf`. |
| empirical_dist([data, operation, new_params, sample_size]) | Compute Empirical distribution related operations, including `fit`, `sample`, `cdf`, `ppf`. |
| select_univariate([data, candidates]) | Evaluate and return the best univariate class for input data using `scipy.stats.kstest`. Use `candidates` to restrict the eligible distributions. |
| fit(data, [candidates, ]) | Wrapper function to fit the input `data` to best distribution, based on `scipy.stats.kstest`. Use `candidates` to restrict the eligible distributions. | 
| pdf_wrapper(data) | Wrapper function to compute PDF given data samples. Use only when class instance has already been fitted to a distribution.|
| cdf_wrapper(data) | Wrapper function to compute CDF given data samples. Use only when class instance has already been fitted to a distribution.|
| ppf_wrapper(data) | Wrapper function to compute PPF given data samples. Use only when class instance has already been fitted to a distribution.|