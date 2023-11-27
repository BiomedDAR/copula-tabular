---
layout: default
title: Tabular Copula
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# TabulaCopula

`class TabulaCopula(definitions=None, output_general_prefix=None, conditionalSettings_dict=None, metaData_transformer=None, var_list_filter=None, removeNull=False, sampling=None, debug=False)`
Module for performing copula/conditional-copula (Gaussian) for Tabular-type data.

### Parameters

**definitions**:  file (.py), optional, default `None`. Contain global variables

**output_general_prefix**: str, optional, default `None`. Prefix used for all output files, e.g. `"EXPT_1"`. If not `None`, replaces settings in `definitions`.

**conditionalSettings_dict**: dict, optional, default `None`. Dictionary of conditional inputs for using conditional-copula.

**metaData_transformer**: dict, optional, default `None`. Dictionary of inputs for the Transformer class initialisation (ref [Transformer](../Transformer/) metaData).

**var_list_filter**: list, optional, default `None`. List of variables to transform. If `None`, all will be transformed.

**removeNull**: boolean, optional, default `False`. Whether to remove all null values prior to transformation. 

**sampling**: float, optional, default `None`. Percentage of sample points draw from the transformed dataframe, leaving the rest as control. If `None`, all training points will be used. (Note that the sampling process is done after the transformation.)

**debug**: boolean, default `True`. Whether to print debug-related outputs to console.

### Notes

#### Description of conditionalSettings_dict
The `conditionalSettings_dict` variable specifies the structure of the conditional setup. It takes the following form:
```
conditionalSettings_dict = {
    "set_1": {
        "bool": True,
        "parent_conditions": { # parents, the `Y` in `P(X | Y)` while learning P(X | Y).
            "SurveyYr": { # split variable into 2 sets
                "condition": "set", #available options: "set", "range"
                "condition_value": {
                    1: ["2009_10"],
                    2: ["2011_12"]
                }
            },
            "Age": { # split variable into 3 sets based on range
                "condition": "range",
                "condition_value": {
                    1: [">=3", "<79"],
                    2: ["<3"],
                    3: [">=79"]
                }
            }
        },
        "conditions_var": ["Age"], # the `Y` to keep constant while generating values of `X` in `P(X | Y)`. Can be a float, in which case it is a threshold to fix all variables with pairwise correlation (with X) above then said threshold.
        "children": ['AgeMonths'] #variable for which to learn the joint conditional distributions on, the `X` in `P(X | Y)`. Can be a string: "allOthers".
    }
}
```

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [Multivariate Synthetic Data (multi-Linear)](../../../gettingStarted/examples/TabulaCopula_conditional) | Demonstrates the use of the TabulaCopula class to generate synthetic data for a multivariate dataset. |
| [Multivariate Synthetic Data (multi-Linear, with missing values)](../../../gettingStarted/examples/TabulaCopula_conditional_2) | Demonstrates use of the TabulaCopula class to generate synthetic data for a multivariate real dataset (NHANES), between variables of known linear relationship. |
| [Multivariate Synthetic Data (multi-Linear, Privacy Leakage Assessment)](../../../gettingStarted/examples/TabulaCopula_conditional_privacyLeakage) | Demonstrates use of the TabulaCopula class to quantitatively assess the privacy leakage risks of generated synthetic data.  |
| [Multivariate Synthetic Data (multi, non-linear, non-monotonic)](../../../gettingStarted/examples/TabulaCopula_conditional_nonmonotonic) | Demonstrates use of the TabulaCopula class to generate synthetic data for a multivariate simulated dataset (socialdata), between variables of known non-linear, non-monotonic relationships. |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug | (boolean) whether to debug or not  |
| folder_trainData | (str) training data folder |
| folder_synData | (str) synthetic data folder |
| folder_privacyMetrics | (str) privacy metrics folder |
| output_general_prefix | (str) prefix used for all output files |
| sampling | (int) percentage of sample points draw from the transformed dataframe, leaving the rest as control |
| privacy_batch_n | (int) number of repetitions of privacy test |
| output_type_data | (str) output file type for the clean data files.  |
| output_type_dict | (str) output file type for the amended dictionary. |
| output_type_obj | (str) output file type for saved class instance |
| dict_var_varname | (str) column in data dictionary containing variable names in input data |
| dict_var_varcategory | (str) column in data dictionary setting the category of the variable name |
| dict_var_vartype | (str) column in data dictionary containing variable types in input data |
| conditional_set_bool | (bool) flag set to true when filenames initialised for conditional setup |
| metaData_transformer | (dict)  dictionary of inputs for the Transformer class initialisation |
| var_list_filter | (list) list of variables to transform (subset of all input variables) |
| removeNull | (bool) Whether to remove all null values prior to transformation.  |
| conditionalSettings_dict | (dict) dictionary of conditional inputs for using conditional-copula.  |
| prefix_path | (str) PREFIX_PATH from definitions  |
| trainxlsx | (str) TRAINXLSX from definitions |
| traindictxlsx | (str) TRAINDICTXLSX from definitions |
| train_data_path | (str) folder path to put training data  |
| train_data_filename | (str) filename of training data  |
| train_data_dict_filename | (str) filename of dictionary of training data |
| syn_data_path | (str) folder path to put synthetic data  |
| privacyMetrics_path | (str) folder path to put privacy metrics  |
| train_df | (dataframe) training data (dataframe) |
| dict_df | (dataframe) data dictionary (dataframe) |
| var_list | (list) list of all variables (column headers) found in input data |
| processed_var_list | (list) list of all variables (column headers) that have been transformed |
| transformed_df | (dataframe) transformed training data (dataframe) / replaced with transformed data after sampling (disjoint with self.control_df)  |
| control_df | (dataframe) dataframe that is not sampled for training (left as control for privacy leakage testing) |
| curated_train_df | (dataframe) curated data prior to transformation (dataframe) |
| syn_samples_df | (dataframe) synthetic samples (dataframe) |
| syn_samples_conditional_df | (dataframe) conditional synthetic samples (dataframe) |
| reversed_df | (dataframe) reversed synthetic samples (dataframe) |
| reversed_conditional_df | (dataframe) conditional reversed synthetic samples (dataframe) |
| reversed_control_df | (dataframe) reversed control_df (dataframe) |
| reversed_transformed_df | (dataframe) reversed transformed_df (dataframe) |
| privacyMetricEval | (obj) privacy metric evaluator |
| privacyMetricEval_cond | (obj) privacy metric evaluator for conditional copula |
| privacyMetricResults | (dict) privacy metric results dictionary |
| definitions |  (obj) definitions in corresponding input `defintions.py` |


### Methods

| Method         | Description | 
| ---:              |    :----   |
| transform([metaData, var_list]) | transform data into numerical equivalent |
| transform_conditional([metaData, ]) | transform data into numerical equivalent (for conditional) |
| reverse_transform([transformed_df, conditional_transformed_df, control_transformed_df]) | reverse transformation on generated synthetic data |
| print_details_copula() | print copula details |
| fit_gaussian_copula([correlation_method, marginal_dist_dict]) | build copula for given training data |
| fit_gaussian_copula_conditional([correlation_method, marginal_dist_dict]) | build conditional-copula for given conditional_dict |
| sample_gaussian_copula([sample_size, conditions]) | sample datapoints from learned joint distribution | 
| sample_gaussian_copula_conditional() | sample datapoints from learned conditional joint distribution | 
| syn_generate([sample_size, cond_bool, conditions]) | wrapper for synthetic data generation |
| build_privacyMetric() | build privacyMetric, privacyMetric_conditional evaluator |
| privacyMetric_singlingOut_Batch([n, mode, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for singling out attack (standard) |
| privacyMetric_singlingOut_cond_Batch([n, mode, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for singling out attack (conditional) |
| privacyMetric_Linkability_Batch(aux_cols, [n, n_neighbors, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for linkability attack (standard) |
| privacyBatch_Linkability_cond_Batch(aux_cols, [n, n_neighbors, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for linkability attack (conditional) |
| privacyMetric_Inference_Batch([n, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for inference attack (standard) |
| privacyMetric_Inference_cond_Batch([n, n_attacks, print_results]) | wrapper fn to run privacy metric evaluation for inference attack (conditional) |
| save() | wrapper fn to save class instance and output filenames |
| save_outputFilenames() | Saves the output filenames dictionary to a csv file, suffix="CL-OF" |
| save_instance() | Saves the current class instance to a pickle file |