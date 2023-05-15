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

### External functions
The CleanData class accepts external/user-specified constraints, in conjunction with the Constraints class.