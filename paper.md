---
title: '<name>: A Python package for conditional synthetic data generation using Copulas'
tags:
  - Python
  - Synthetic Data
  - copulas
  - multidimensional
  - conditional joint probabilities
authors:
  - name: MZ Tan
    orcid: 0000-0003-3200-8341
    corresponding: true # (This is how to denote the corresponding author)
    equal-contrib: true
    affiliation: 1
    # affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Wing-Cheong Wong
    orcid: 0000-0003-1247-6279
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
  # - name: Author with no affiliation
  #   affiliation: 3
affiliations:
 - name: Bioinformatics Institute, A*STAR
   index: 1
#  - name: Institution Name, Country
#    index: 2
#  - name: Independent Researcher, Country
#    index: 3
date: 16 December 2023
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

Recent advancements in synthetic data generation have made it a viable solution for applications in various fields, such as finance, biomedical research [@dahmen2019synsys], and data science[@raghunathan2021synthetic]. Synthetic data is generated artificially, yet replicates the joint probability distribution of its real-world counterpart. Its ability to mimic the statistical behaviour of real data makes it a useful tool for testing algorithms, systems, and training machine learning models, and it can be used as an economical substitute for real data when it is not available, is too sensitive to release, or too costly to acquire. Copula-based data generation methods [@li2014differentially;@li2020sync;kamthe2021copula;@patki2016synthetic] have been demonstrated to produce reliable and accurate tabular data when generating synthetic data, particularly for small datasets where generative methods would otherwise require large number of datapoints.

# Statement of need

In this software, we present an improved version of the copula tools as seen in Synthetic Data Vault (SDV) [@patki2016synthetic], a widely used tool for generating multivariate synthetic data through Gaussian copulas. This enhanced model incorporates conditional joint distributions into its framework, allowing for the splitting of single variables into multiple component marginal distributions (not to be confused with conditional sampling). To the best of our knowledge, this is the first implementation of conditional copula in Python. The improved version of the SDV provides greater usability in the synthesis of complex, non-linear, non-monotonic sample distributions (see Fig.\autoref{fig:scatterplots}), and stronger replication of correlation between variables (see Fig. \autoref{fig:correlationplots}), allowing for the replication of a wider range of tabular datasets.

Our enhancement is written entirely in Python and is designed to work with a data dictionary (specifying the metadata of the input dataset). There are additional class-based implementations of preprocessing tools such as data cleaning, transformation tools, post-processing tools for easy visualisation of results, privacy leakage evaluation, and sample wrapper scripts for generating synthetic data from start to finish.



# Figures

![Figure showing correlation plots of a simulated multivariate dataset, containing non-trivial, non-linear and non-monotonic relationships. The left plot shows the original Pearson correlation between variables, while the middle and right plots show the correlation for synthetic data generated using standard copula and conditional copula respectively. \label{fig:correlationplots}](docs/assets/img/tabulaCopula_example_socialdata_correlation_matrix_three.svg)

![Figure showing superimposed scatterplots of the same simulated multivariate dataset, containing non-trivial, non-linear and non-monotonic relationships. The training, synthetic (standard copula), synthetic (conditional copula) data points are in blue, grey, and red respectively. \label{fig:scatterplots}](docs/assets/img/tabulaCopula_example_socialdata_scatterplot_lowsampling_six.svg)


<!-- # Acknowledgements -->


# References