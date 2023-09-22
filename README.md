# copula-tabular
Generate tabular synthetic data using Gaussian copulas

<div align="center">

  [Overview](#overview) | [Documentation](#documentation) | [How to cite](#how-to-cite) | [Contributing](#contributing) | [Development notes](#development-notes) | [Copyright and license](#copyright-and-license) | [Acknowledgements](#acknowledgements)
</div>

## Overview

Advancements in synthetic data generation have made it a viable solution for applications in various fields, such as finance, biomedical research, and data science. Synthetic data is generated artificially, yet replicates the joint probability distribution of its real-world counterpart. Its ability to mimic the statistical behaviour of real data makes it a useful tool for testing algorithms, systems, and training machine learning models, and it can be used as an economical substitute for real data when it is not available, is too sensitive to release, or too costly to acquire. Copula-based data generation methods have been demonstrated to produce reliable and accurate tabular data when generating synthetic data.

In this package, we present a tool for generating multivariate synthetic data through the implementation of a Gaussian copula. This model incorporates conditional joint distributions into its framework, allowing for the splitting of single variables into multiple component marginal distributions. The conditional enhancements provides greater usability in the synthesis of complex, non-linear sample distributions, allowing for the replication of a wider range of datasets.

The tool is designed to work with a data dictionary, or a file describing the metadata of the input dataset. There are additional class-based implementations of data cleaning, visualisation tools, transformation tools, and sample wrapper scripts for generating synthetic data from start to finish.

## Documentation
For installation instructions, getting started guides and tutorials, background information, and API reference summaries, please see the 
[website](https://biomeddar.github.io/copula-tabular/).

## How to cite

## Contributing

## Development notes

## Copyright and license
Copyright 2023 BiomedDAR, BII, A*STAR. Licensed under [MIT](LICENSE.txt).

## Acknowledgements