---
layout: default
title: Definitions (List of global variables)
parent: Getting Started
nav_order: 5
---

# Definitions (List of Global Variables)

| Attribute         | Description | Type    |
| ---:              |    :----    | :----   |
| PREFIX_PATH       | Defines the root directory path  | Directory |
| RAW_PATH          | Define folder name for all raw data files | Directory |
| TRAIN_PATH        | Define folder name for all cleaned data files. If not specified, default is `"trainData"` | Directory |
| READ_NA           | Option for loading CSVs. If `False`, data entries that can be found in default nanList will be converted to `NaN`. If `True`, above entries will be preserved as they are. If not specified, default is `False` | Data loading |
| RAWXLSX           | Defines filename containing the raw data. E.g. "xx.xlsx", "xx.csv" | Data loading |
| RAWXLSX_SHEETNAME | if RAWXLSX is an excel file, assign the sheetname from which to load the data. If not specified, will read the first sheet. E.g. "Sheet1" | Data loading |
| RAWDICTXLSX       | Defines filename containing the data dictionary. E.g. "xx.xlsx", "xx.csv" | Data loading |
| RAWDICTXLSX_SHEETNAME | if RAWDICTXLSX is an excel file, assign the sheetname from which to load the dictionary. If not specified, will read the first sheet. E.g. "Sheet1" | Data loading |
| LOGGING           | Option to output logfile. If `True`, logfile will be built. If not specified, default is `True`. | Log | 
| LOG_FILENAME      | Defines filename of logfile. If not defined, default is `logfile.txt`. |
| LONG_VAR_MARKER   | Defines the variable name that indicates which longitudinal group that row belongs to. If not specified, default is `None`. | Longitudinal data |
| DICT_VAR_VARNAME  | Column in data dictionary containing variable names in input data. If not specified, set as "`NAME`". | Data Dictionary settings |
| DICT_VAR_VARCATEGORY | Column in data dictionary setting the category of the variable name. If not specified, set as "`CATEGORY`" | Data Dictionary settings |
| DICT_VAR_TYPE | Column in data dictionary setting the type of variable (string, numeric, date). If not specified, set as "`TYPE`" | Data Dictionary settings |
| DICT_VAR_CODINGS | Column in data dictionary setting the codings of variable (dateformat, categories). If not specified, set as "`CODINGS`" | Data Dictionary settings |
| VAR_NAME_STRIPEMPTYSPACES | Boolean option. If `True`, empty spaces will be stripped from variable names in input data, and from variables names listed in data dictionary. If not specified, default is `False`. | Data cleaning settings |
| OUTPUT_TYPE_DATA | The output file type for the clean data files. Available options: '`csv`', '`xlsx`'. If not specified, default is '`csv`' | Data cleaning settings |
| OUTPUT_TYPE_DICT | The output file type fot the amended dictionary. Available options: '`csv`', '`xlsx`'. If not specified, default is '`xlsx`' | Data cleaning settings |
| SUFFIX_DROPPED_DUPLICATED_ROWS | The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `DD`. | Drop Duplicates settings |
| OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME | The output filename to store the duplicated rows which have been dropped. Default is `rowsRemoved.xlsx` | Drop Duplicates settings |
| SUFFIX_CONSTRAINTS | The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `CON`. | Constraints settings |
| SUFFIX_STANDARDISE_TEXT | The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `ST`. | Standardise Text settings |
| OPTIONS_STANDARDISE_TEXT_CASE_TYPE | The default case type to convert strings into: "uppercase", "lowercase", "capitalise". If not specified, default is `uppercase`. | Standardise Text settings |
| OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST | The variables to exclude from the conversion. For example: `["Gender", "Work"]`. | Standardise Text settings |
| OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT | The dictionary to customise case_type for specific variables, overwriting default. For example: `{"Race1": "capitalise"}`. | Standardise Text settings |
| SUFFIX_STANDARDISE_DATE | The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `DATE`. | Date standardisation settings |
| OPTIONS_STANDARDISE_DATE_FORMAT | The standard date format to use for all dates (if not specified, default is `yyyy-mm-dd`). Follows format used in ms-excel, see [ref](https://www.ablebits.com/office-addins-blog/change-date-format-excel/). Example: `ddd, dd mmmm yy`. | Date standardisation settings |
| OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME | The filename for storing list of failed date conversions (only csv). Default is `failed_date_conversions.csv`. | Date standardisation settings |
| SUFFIX_CONVERT_ASCII | The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `ASCII`. | ASCII Conversion settings |
| OPTIONS_CONVERT_ASCII_EXCLUSION_LIST | List of characters to exclude from conversion. Eg. `['€','$','Ò']`. | ASCII Conversion settings |