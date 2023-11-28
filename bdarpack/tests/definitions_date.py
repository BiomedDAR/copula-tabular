# USE THIS SCRIPT TO SET DEFINITIONS
# PUT THIS SCRIPT AT ROOT 

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

PREFIX_PATH = f"{dir_path}\\" # Define the root directory

# SET GLOBAL VARIABLES FOR RAW DATA FILES
RAW_PATH = "rawData" # Set the folder name for all raw data files
TRAIN_PATH = "trainData" # Set the folder name to store all the cleaned data files. If not specified, default is "trainData"

RAWXLSX = "date_dataset.xlsx" # filename containing the raw data
RAWXLSX_SHEETNAME = "Sheet1" # if RAWXLSX is an excel file, assign the sheetname from which to load the data. If not specified, will read the first sheet.

RAWDICTXLSX = "date_dataset_dict.xlsx" #filename containing the data dictionary
RAWDICTXLSX_SHEETNAME = "Sheet1" # if RAWDICTXLSX is an excel file, assign the sheetname from which to load the dictionary. If not specified, will read the first sheet.

# SETTINGS FOR LONGITUDINAL DATA
LONG_VAR_MARKER = None # The variable name that indicates which longitudinal group that row belongs to. If not specified, default is None.

# SETTINGS FOR DATA DICTIONARY
DICT_VAR_VARNAME = "NAME" # column in data dictionary containing variable names in input data. If not specified, set as "NAME".
DICT_VAR_VARCATEGORY = "CATEGORY" # column in data dictionary setting the category of the variable name. If not specified, set as "CATEGORY"
DICT_VAR_TYPE = "TYPE" # column in data dictionary setting the type of variable (string, numeric, date). If not specified, set as "TYPE"
DICT_VAR_CODINGS = "CODINGS" # column in data dictionary setting the codings of variable (dateformat, categories). If not specified, set as "CODINGS"

# SETTINGS FOR DATA CLEANING
VAR_NAME_STRIPEMPTYSPACES = True # option. If True, empty spaces will be stripped from variable names in input data, and from variables names listed in data dictionary. If not specified, default is False.

OUTPUT_TYPE_DATA = 'csv' # the output file type for the clean data files. Available options: 'csv', 'xlsx'. If not specified, default is 'csv'
OUTPUT_TYPE_DICT = 'xlsx' # the output file type fot the amended dictionary. Available options: 'csv', 'xlsx'. If not specified, default is 'xlsx'

# SETTINGS FOR DATE STANDARDISATION
# note that the CODINGS specification is used to specify the date format of the raw dataset, NOT the desired date format. The desired date format is specified using the OPTIONS_STANDARDISE_DATE_FORMAT global variable. When the specified date format under CODINGS causes an error in a specific row, the output will be NaN.
# note that if the data is in excel format, and the date column is specified as some date format, CODINGS specification is ignored.
SUFFIX_STANDARDISE_DATE = "DATE"
OPTIONS_STANDARDISE_DATE_FORMAT = 'ddd, dd mmmm yy' # the standard date format to use for all dates (if not specified, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]
OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME = 'failed_date_conversions.csv' # file location for storing list of failed date conversions (only csv)

# SETTINGS FOR ASCII CONVERSION
SUFFIX_CONVERT_ASCII = "ASCII"
OPTIONS_CONVERT_ASCII_EXCLUSION_LIST = ['€','$','Ò'] # list of characters to exclude from conversion