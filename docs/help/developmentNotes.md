---
layout: default
title: Development notes
parent: Help and Reference
nav_order: 4
---

# Testing

Automated testing is available for `CleanData` and `Transformer`

Testing CleanData Class:
```
python -m bdarpack.tests.test_clean -v
```

Testing Transformer Class:
```
python -m bdarpack.tests.test_transformer -v
```

Automated testing of the final output is difficult for synthetic data generation modules, due to the nature of random sampling. However, users can follow the detailed steps in the [Examples](../gettingStarted/examples/) section to verify expected functionality of other features, including
*   generating synthetic data for multivariate, non-monotonic, non-linear data
*   generating synthetic data for univariate data
*   checking privacy leakage
*   simple Gaussian copula

Source/Raw input files, intermediate results, and test scripts are included in the GitHub source code, under the `examples` folder.