---
layout: default
title: Example for Multivariate Synthetic Data (multi, non-linear, non-monotonic)
parent: Examples
grand_parent: Getting Started
nav_order: 11
---

### Example of TabulaCopula Class
This example demonstrates the use of the TabulaCopula class to generate synthetic data for a multivariate simulated dataset (socialdata), between variables of known non-linear, non-monotonic relationships.

The dataset contains 7 simulated variables with the following relationships:
#### Plot of all relationships between 7 simulated variables
![](../../assets/img/tabulaCopula_example_socialdata_original_scatterplot.png)

### Import Libraries
```
import sys, os
import matplotlib.pyplot as plt
import pickle

# ADD PATH  (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)
head, sep, tail = dir_path.partition('copula-tabular')
sys.path.insert(0, head+sep) # adding par_dir to system path

from mz.TabulaCopula import TabulaCopula
from mz import VIsualPlot as vp
from mz import utils_ as ut_
```

### Load script containing definitions
The definitions.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined. It contains the paths, filenames, prefixes, and options to the inputs and outputs of the pipeline.

Refer to the sample definitions_script_3.py provided for detailed guidance on individual attributes.

```
import definitions_script_3 as defi
```

### Initialise the TabulaCopula class with definitions
With the loaded definitions, we can initialise our TabulaCopula class. Prior to that, we can define a few other settings.

Like before, we can initiate the transformation of the variables to numerical equivalents of our liking using a `meteData_transformer` dict. This step is relatively simple (i.e. can be ignored) for this dataset because all the variables are already numeric. There are also no `null` variables.

```
metaData_transformer = None
```

If we are not using the conditional-copula setup, we can ignore the `conditionalSettings_dict` option, or set it to `None`. We set a flag so that we can turn this option `on` and `off` easily. 

For convenience, we set three flags, namely `run_syn`, `cond_bool`, and `visual`, to run the synthetic data generation algorithm, use conditional settings, and plot results, respectively. It is not necessary to run the algorithm everytime just to plot results, or perform privacy leakage tests on the generated data, since we can easily save it in a pickle file for future use.

```
run_syn = True
cond_bool = True
visual = True
```

We set three different sets of conditions, and will be running them in sequence, on top of a set of baseline synthetic data, generated without conditions. 
The first set `set_1-0` is equivalent to a baseline set where the `Age` variable is split into intervals of `10` years each. Essentially, we will be splitting the dataset into different subject groups and learning their joint distributions `P_i(X,Y)` separately, before re-sampling the `children` variables `(X)` based on the new joint distributions, conditional on `conditions_var` variables `(Y)`, i.e. `P_i(X|Y)`.
```
if cond_bool:
    # LOAD CONDITIONAL SETTINGS
    conditionalSettings_dict = {
        "set_1-0": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": ut_.gen_dict_range_interval(interval=10, min_num=30, max_num=90)
                }
            },
            "conditions_var": ["Age"],
            "children": "allOthers"
        },
        "set_1-1": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": ut_.gen_dict_range_interval(interval=5, min_num=30, max_num=90)
                }
            },
            "conditions_var": ["Age"],
            "children": ["Asset"]
        },
        "set_1-2": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": {
                        1: [">=30", "<40"],
                        2: [">=40", "<50"],
                        3: [">=50", "<53"],
                        4: [">=53", "<73"],
                        5: [">=73", "<90"],
                    }
                }
            },
            "conditions_var": ["Age"],
            "children": ["Satisfaction"]
        },
        "set_2-1": { #when AgeGroup is available
            "bool": False,
            "parent_conditions": {
                "AgeGroup":{
                    "condition": "set",
                    "condition_value": {
                        1: ["1"],
                        2: ["2"],
                        3: ["3"]
                    }
                }
            },
            "conditions_var": 0.5,
            "children": "allOthers"
        }
    }
else:
    conditionalSettings_dict = None
```