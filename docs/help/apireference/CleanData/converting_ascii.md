---
layout: default
title: Converting ASCII
parent: Clean Data
grand_parent: API Reference
nav_order: 5
---

# CleanData.converting_ascii

Standardises text case in input data.

**CleanData.converting_ascii([*ascii_exclusion_list* ,])**

**Parameters**
- *ascii_exclusion_list*: (list, optional)
  - List of characters to not replace
  - default: `self.options_convert_ascii_exclusion_list`

**Returns**
None.

### Notes
*   Update dataframe can be found as `CleanData.clean_df`.
*   A copy of the cleaned data can be found in the folder `CleanData.train_data_path`, with a suffix `CleanData.suffix_convert_ascii`.

#### Relevant Definitions Settings
* **SUFFIX_CONVERT_ASCII**: suffix to append to the end of the output filename of the input data. E.g. "`ASCII`"
* **OPTIONS_CONVERT_ASCII_EXCLUSION_LIST**: list of characters to exclude from conversion. E.g. "`['€','$','Ò']`".

### Examples
See Example [cleanData](../../../gettingStarted/examples/CleanData_StandardiseDates_ConvertCharacters) for detailed setup and outputs.