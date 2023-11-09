---
layout: default
title: CleanData
parent: API Reference
grand_parent: Help and Reference
nav_order: 2
---

# CleanData

`class CleanData(definitions=None, debug=True)`

Module for data cleaning. Designed to work with a data dictionary (metadata). See [template](../../assets/datadict/Data%20Dictionary%20Documentation/template_dict_nhanes.xlsx) and [guide](../../assets/datadict/Data%20Dictionary%20Documentation/Data%20Dictionary%20Manual.docx) for more details.

### Parameters

**definitions**: file (.py) containing global variables

#### Global variables for raw data files
*   `PREFIX_PATH`: define the root directory
*   `RAW_PATH`: set the folder name for all raw data files
*   `TRAIN_PATH`: set the folder name to store all the cleaned data files. If not specified, default is "`trainData`"
*   `RAWXLSX`: filename containing the raw data
*   `RAWXLSX_SHEETNAME`: if RAWXLSX is an excel file, assign the sheetname from which to load the data. If not specified, will read the first sheet.
*   `RAWDICTXLSX`: filename containing the data dictionary
*   `RAWDICTXLSX_SHEETNAME`: if RAWDICTXLSX is an excel file, assign the sheetname from which to load the dictionary. If not specified, will read the first sheet.

#### Settings for Longitudinal data
*   `LONG_VAR_MARKER`: (in preparation for longitudinal data) the variable name that indicates which longitudinal group that row belongs to. If not specified, default is `None`.

#### Settings for Data Dictionary
*   `DICT_VAR_VARNAME`: column in data dictionary containing variable names in input data. If not specified, set as "`NAME`".
*   `DICT_VAR_VARCATEGORY`: column in data dictionary setting the category of the variable name. If not specified, set as "`CATEGORY`"
*   `DICT_VAR_TYPE`: column in data dictionary setting the type of variable (string, numeric, date). If not specified, set as "`TYPE`"
*   `DICT_VAR_CODINGS`: column in data dictionary setting the codings of variable (dateformat, categories). If not specified, set as "`CODINGS`"

#### Settings for Data Cleaning
*   `VAR_NAME_STRIPEMPTYSPACES`: boolean option. If `True`, empty spaces will be stripped from variable names in input data, and from variables names listed in data dictionary. If not specified, default is `False`.
*   `OUTPUT_TYPE_DATA`: the output file type for the clean data files. Available options: '`csv`', '`xlsx`'. If not specified, default is '`csv`'
*   `OUTPUT_TYPE_DICT`: the output file type fot the amended dictionary. Available options: '`csv`', '`xlsx`'. If not specified, default is '`xlsx`'

#### Settings for Drop Duplicates
*   `SUFFIX_DROPPED_DUPLICATED_ROWS`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `DD`.
*   `OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME`: output file name to store the duplicated rows which have been dropped. Default is `rowsRemoved.xlsx`

#### Settings for Constraints
*   `SUFFIX_CONSTRAINTS`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `CON`.

#### Settings for Standardise Text
*   `SUFFIX_STANDARDISE_TEXT`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `ST`.
*   `OPTIONS_STANDARDISE_TEXT_CASE_TYPE`: default case type to convert strings into: "uppercase", "lowercase", "capitalise". If not specified, default is `uppercase`.
*   `OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST`: variables to exclude from the conversion. For example: `["Gender", "Work"]`
*   `OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT`: dictionary to customise case_type for specific variables, overwriting default. For example: `{"Race1": "capitalise"}`.

#### Settings for Date Standardisation
*   `SUFFIX_STANDARDISE_DATE`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `DATE`.
*   `OPTIONS_STANDARDISE_DATE_FORMAT`: the standard date format to use for all dates (if not specified, default is `yyyy-mm-dd`). Follows format used in ms-excel, see [ref](https://www.ablebits.com/office-addins-blog/change-date-format-excel/)Example: `ddd, dd mmmm yy`.
*   `OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME`: filename for storing list of failed date conversions (only csv). Default is `failed_date_conversions.csv`

#### Settings for ASCII Conversion
*   `SUFFIX_CONVERT_ASCII`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `ASCII`.
*   `OPTIONS_CONVERT_ASCII_EXCLUSION_LIST`: List of characters to exclude from conversion. Eg. `['€','$','Ò']`

**debug**: boolean, default None

&emsp;If `True`, print intermediate outputs for debugging purposes

### Notes

### Examples

### Attributes

### Methods