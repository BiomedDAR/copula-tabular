---
layout: default
title: Features
parent: Getting Started
nav_order: 2
---

## CleanData Class
The CleanData class facilitates data preparation for synthetic data generation. It takes raw input data as input and prepares it for use in generating synthetic data. It comprises the following features:

### Organised Outputs
Output files are generated for each cleaning step and are collected in a user-defined folder (default: `trainData`). 
Filenames are appended with suffixes (e.g. `DD`, `CON`), in the order with which they are processed. This designation is useful in cases where the cleaning sequence generates different outputs.

### In-built functions
The CleanData class comprises several in-built functions:
*   strips all leading/trailing empty spaces from variable names
*   verifies variable names in input data against meta information in data dictionary
*   drops duplicate rows
*   standardise text format (capital/small letters)
*   converts all characters to ASCII-compatible alternatives
*   standardise date format
*   rudimentary report of data (number of missing values, range, data-type, etc...)

### External functions
The CleanData class accepts external/user-specified constraints, in conjunction with the Constraints class.

## Transformer Class
The Transformer class converts raw-data/cleaned data (ref. CleanData class) into its numerical equivalent for processing with Copulas. Available transformation methods include:
*   computation of fill values for `null' entries using mean, mode, median methods
*   transformation of categorical to numerical values using `One-Hot`, `LabelEncoding`, `Representative floats`, or `Representative floats (fuzzy)`
*   transformation of standardised datetype data into numerical representation
*   transformation reversal to recover original data

## MarginalDist Class
The MarginalDist Class fits data columns with individual marginal distributions. Available methods include:
*   parametric distributions: beta, laplace, loglaplace, gamma, gaussian, student_t, uniform
*   non-parametric distributions: empirical, gaussian_kde, degenerate
*   automatic selection of best univariate distribution using KS-Test
*   generation of PDF, CDF, PPF for all distributions

## GaussianCopula Class
The GaussianCopula Class fits a Gaussian copula on a given multivariate dataset. Available methods include:
*   copula-fitting
*   sampling from fitted multivariate joint distribution
*   sampling from fitted multivariate joint distribution given conditions

## TabulaCopula Class
Wrapper that fits conditional-copulas on a given multivariate dataset. Available methods include:
*   conditional copula-fitting
*   sampling from conditionally-fitted multivariate joint distribution