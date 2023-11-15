---
layout: default
title: Drop Duplicate Rows
parent: Clean Data
grand_parent: API Reference
nav_order: 3
---

# CleanData.drop_duplicate_rows

Use to drop duplicate rows from the input dataframe. Performs the following steps:

1.  Exclude variables of the "Index" category from the duplicate search
1.  Make a working copy of the input dataframe
1.  Get the index of duplicate rows
1.  Drop the duplicate rows from the dataframe
1.  Get the dropped rows from the original dataframe and save them as an excel file (`CleanData.dropped_duplicated_rows_filename`)
1.  Update the new filename and the new input dataframe (suffix used: `CleanData.suffix_dropped_duplicated_rows`)

**CleanData.drop_duplicate_rows()**

**Parameters**
None.

**Returns**
None.

### Notes
*   Update dataframe can be found as `CleanData.clean_df`.
*   A copy of the cleaned data can be found in the folder `CleanData.train_data_path`, with a suffix `CleanData.suffix_dropped_duplicated_rows`.
*   A record of the dropped rows can be found in the folder `CleanData.train_data_path`, with the filename `CleanData.dropped_duplicated_rows_filename`.

#### Relevant Definitions Settings
* **SUFFIX_DROPPED_DUPLICATED_ROWS**: suffix to append to the end of the output filename of the input data. E.g. "`DD`"
* **OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME**: output file name to store the duplicated rows which have been dropped. E.g. "`rowsRemoved.xlsx`".


### Examples
See Example [cleanData](../../../gettingStarted/examples/CleanData) for detailed setup and outputs.