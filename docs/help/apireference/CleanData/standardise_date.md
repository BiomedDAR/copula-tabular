---
layout: default
title: Standardise Date
parent: Clean Data
grand_parent: API Reference
nav_order: 6
---

# CleanData.standardise_date

Standardises the date/time in input data.

Standardise the date format of variables of the TYPE "date" (as specified in the data dictionary). Primarily changes the format of the column as per the predefined standard date and time format, as specified in `OPTIONS_STANDARDISE_DATE_FORMAT` (global definitions).

It also stores the failed conversions in a csv file, as specified in `OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME` (global definitions)

**CleanData.standardise_date([*def_date_format*, *faileddate_conversions_filename* ])**

**Parameters**
- *def_date_format*: (string, optional)
  - the standard date format to use for all dates (ignore if already specified in global definitions) It follows format used in ms-excel, see [ref](https://www.ablebits.com/office-addins-blog/change-date-format-excel/).
  - default: `yyyy-mm-dd`
- *faileddate_conversions_filename*: (string, optional)
  - the filename.csv for storing list of failed date conversions (ignore if already specified in global definitions).
  - default: `failed_date_conversions.csv`

**Returns**
None.

### Notes
*   Updated dataframe can be found as `CleanData.clean_df`.
*   A copy of the cleaned data can be found in the folder `CleanData.train_data_path`, with a suffix `CleanData.suffix_standardise_date`.
*   Only `csv` file format allowed for `faileddate_conversions_filename`.
*   The `CODINGS` in the data dictionary is used to specify the date format of the raw dataset, NOT the desired date format. The desired date format is specified using the `OPTIONS_STANDARDISE_DATE_FORMAT` global variable. When the specified date format under `CODINGS` causes an error in a specific row, the output will be `NaN`.
*   If the data is in excel format, and the date column is specified as some date format (according to excel specifications), `CODINGS` specification is ignored.

#### Relevant Definitions Settings
* **SUFFIX_STANDARDISE_DATE**: suffix to append to the end of the output filename of the input data. E.g. "`DATE`"
* **OPTIONS_STANDARDISE_DATE_FORMAT**: the standard date format to use for all dates. E.g. "`ddd, dd mmmm yy`".
* **OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME**: file location for storing list of failed date conversions (only csv). E.g. "`failed_date_conversions.csv`".

### Examples
See Example [cleanData](../../../gettingStarted/examples/CleanData_StandardiseDates_ConvertCharacters) for detailed setup and outputs.