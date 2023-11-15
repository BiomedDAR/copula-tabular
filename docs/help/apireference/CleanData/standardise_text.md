---
layout: default
title: Standardise Text
parent: Clean Data
grand_parent: API Reference
nav_order: 4
---

# CleanData.standardise_text

Standardises text case in input data.

**CleanData.standardise_text()**

**Parameters**
None.

**Returns**
None.

### Notes
*   Update dataframe can be found as `CleanData.clean_df`.
*   A copy of the cleaned data can be found in the folder `CleanData.train_data_path`, with a suffix `CleanData.suffix_standardise_text`.

#### Relevant Definitions Settings
* **SUFFIX_STANDARDISE_TEXT**: suffix to append to the end of the output filename of the input data. E.g. "`SS`"
* **OPTIONS_STANDARDISE_TEXT_CASE_TYPE**: default case type to convert strings into. options: "uppercase", "lowercase", "capitalise". E.g. "`uppercase`".
* **OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST**: list of variables to exclude from the conversion. E.g. "`["Gender", "Work"]`".
* **OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT**: dictionary to customise case_type for specific variables, overwriting default. E.g. "`{"Race1": "capitalise"}`".

### Examples
See Example [cleanData](../../../gettingStarted/examples/CleanData) for detailed setup and outputs.