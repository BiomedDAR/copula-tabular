---
layout: default
title: Clean Data
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# CleanData

`class CleanData(definitions=None, debug=True)`
Module for data cleaning. Designed to work with a data dictionary (metadata). See data dictionary [template](../../../assets/datadict/Data%20Dictionary%20Documentation/template_dict_nhanes.xlsx) and data dictionary [guide](../../../assets/datadict/Data%20Dictionary%20Documentation/Data%20Dictionary%20Manual.docx) for more details.

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

#### Settings for Log Files
*   `LOGGING`: A boolean. Whether to output logfile or not. If not specified, default is `True`.
*   `LOG_FILENAME`: A string. Filename of log file. If not defined, default is "`logfile.txt`".

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
*   `OPTIONS_STANDARDISE_DATE_FORMAT`: the standard date format to use for all dates (if not specified, default is `yyyy-mm-dd`). Follows format used in ms-excel, see [ref](https://www.ablebits.com/office-addins-blog/change-date-format-excel/). Example: `ddd, dd mmmm yy`.
*   `OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME`: filename for storing list of failed date conversions (only csv). Default is `failed_date_conversions.csv`

#### Settings for ASCII Conversion
*   `SUFFIX_CONVERT_ASCII`: The filename suffix to use for intermediate outputs of cleaned data. If not specified, default is `ASCII`.
*   `OPTIONS_CONVERT_ASCII_EXCLUSION_LIST`: List of characters to exclude from conversion. Eg. `['€','$','Ò']`

**debug**: boolean, default None

&emsp;If `True`, print intermediate outputs for debugging purposes

### Notes

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [cleanData 1](../../../gettingStarted/examples/CleanData) | Demonstrates use of `definitions.py`, dropping duplicate rows, and standardising text variables (capital/small letters) |
| [CleanData 2](../../../gettingStarted/examples/CleanData_StandardiseDates_ConvertCharacters) | Demonstrates use of `definitions.py`, standardising date formats, conversion of characters from international accents to ASCII-compatible symbols |
| [CleanData 3](../../../gettingStarted/examples/CleanDataWithConstraints) | Demonstrates use of customised constraints |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug             | (boolean) whether to debug or not      |
| definitions       | (obj) definitions in corresponding input `defintions.py`      |
| dict_df           | (dataframe) data dictionary      |
| raw_df            | (dataframe) raw data |
| clean_df          | (dataframe) cleaned data       |
| clean_dict_df     | (dataframe) cleaned data dictionary       |
| report_df         | (dataframe) report
| cat_var_dict      | (dict) with categories as keys and the respective variables as values, {cat: [list of variables]}       |
| type_var_dict     | (dict) with the variable type as keys and the respective variables as values
| longitudinal_marker_list | (list) list of longitudinal markers
| longitudinal_variableMarker | (str) column header which contains the list of categories stipulating a list of longitudinal markers
| dict_var_codings         | (str) column name in data dict. setting the codings of the variable e.g. `"CODINGS"`       |
| dict_var_type         | (str) column name in data dict. setting the type of variable e.g. `"TYPE"`       |
| dict_var_varcategory         | (str) column name in data dict. setting the category of the variable name e.g. `"CATEGORY"`       |
| dict_var_varname         | (str) column name in data dict containing variable names in input data e.g. `"NAME"`       |
| raw_data_dict_filename | (str) full path of original data dictionary |
| raw_data_dict_sheetname | (str) sheet name of original data dictionary |
| raw_data_filename | (str) full path of raw data |
| raw_data_sheetname | (str) sheet name of raw data |
| raw_data_path | (str) full path of folder storing raw data | 
| train_data_path | (str) full path of folder storing training data | 
| folder_rawData           | (str) folder storing raw data, e.g. `"rawData"`       |
| folder_trainData         | (str) folder storing training data (outputs of cleaning modules), e.g. `"trainData"`       |
| data_latest_filename     | (str) latest filename for cleaned data       |
| dict_latest_filename     | (str) latest filename for cleaned data dictionary       |
| dropped_duplicated_rows_filename     | (str) filename for storing dropped duplicate rows    |
| initial_report_filename      | (str) filename for storing report    |
| log_filename      | (str) filename for storing logs    |
| log_filepath      | (str) full path of `log_filename`    |
| logger            | (obj) logger to pass on for logging |
| logging           | (boolean) whether to do logging or not |
| options_convert_ascii_exclusion_list | (list) list of symbols to exclude from ASCII conversion |
| options_faileddate_conversions_filename | (str) filename for storing list of failed date conversions |
| options_standardise_date_format | (str) date standardisation format e.g. `"yyyy-mm-dd"` |
| options_standardise_text_case_type | (str) option for standardising case format, e.g. `"uppercase"`|
| options_standardise_text_case_type_dict | (dict) dictionary to customise case_type for specific variables. |
| options_standardise_text_exclude_list | (list) variables to exclude from the conversion |
| output_type_data | (str) the output file type for the clean data files |
| output_type_dict | (str) the output file type fot the amended dictionary |
| prefix_path | (str) prefix path as stipulated in dictionary |
| suffix_constraints | (str) suffix to append to `data_latest_filename` after applying constraints |
| suffix_convert_ascii | (str) suffix to append to `data_latest_filename` after converting ASCII symbols |
| suffix_dropped_duplicated_rows | (str) suffix to append to `data_latest_filename` after dropping duplicate rows |
| suffix_standardise_date | (str) suffix to append to `data_latest_filename` after standardising dates |
| suffix_standardise_text | (str) suffix to append to `data_latest_filename` after standardising text case |
| var_diff_list | (list) list of mismatched variable names between input data and data dictionary | 
| var_list | (list) list of all variables (column headers) found in input data
| var_name_stripemptyspaces | (boolean) if `True`, empty spaces will be stripped from variable names in input data, and from variables names listed in data dictionary. |


### Methods

| Method         | Description | 
| ---:              |    :----   |
| convert_2_dtypes(data) | Convert data (df) into best possible dtypes. |
| [gen_data_report(data, dict)](gen_data_report) | Generates a report of `data` |
| [drop_duplicate_rows()](drop_duplicate_rows) | Use to drop duplicate rows from the input dataframe. |
| standardise_text_case_conversion(data, case_type) | Takes dataframe (cols) and one case type parameter as input and returns the text data converted as per the case type specified. |
| [standardise_text()](standardise_text) | Standardises text case in input data. |
| [converting_ascii([ascii_exclusion_list, ])](converting_ascii) | Converts all characters in input data to ASCII-compatible format. |
| [standardise_date([def_date_format, faileddate_conversions_filename])](standardise_date) | Standardises the date/time in input data. |

