# USE THIS SCRIPT TO SET DEFINITIONS
# PUT THIS SCRIPT AT ROOT 

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

PREFIX_PATH = f"{dir_path}\\" # Define the root directory

# SET GLOBAL VARIABLES FOR DATA FILES
RAW_PATH = "rawData" # Set the folder name for all raw data files
TRAIN_PATH = "trainData" # Set the folder name to store all the cleaned data files. If not specified, default is "trainData"
SYN_PATH = "synData" #Set the folder name to store all the synthetic data files. If not specified, default is "synData"

# TRAINING DATA FILES
TRAINXLSX = "nhanes_raw-DD-CON-ST.csv" # filename containing the raw data
TRAINXLSX_SHEETNAME = "Sheet1" # if RAWXLSX is an excel file, assign the sheetname from which to load the data. If not specified, will read the first sheet.

TRAINDICTXLSX = "nhanes_dict_2-1.xlsx" #filename containing the data dictionary
TRAINDICTXLSX_SHEETNAME = "Sheet1" # if RAWDICTXLSX is an excel file, assign the sheetname from which to load the dictionary. If not specified, will read the first sheet.

# SETTINGS FOR DATA DICTIONARY
DICT_VAR_VARNAME = "NAME" # column in data dictionary containing variable names in input data. If not specified, set as "NAME".
DICT_VAR_VARCATEGORY = "CATEGORY" # column in data dictionary setting the category of the variable name. If not specified, set as "CATEGORY"
DICT_VAR_TYPE = "TYPE" # column in data dictionary setting the type of the variable . If not specified, set as "TYPE"

OUTPUT_GENERAL_PREFIX = "" # prefix used for all output files, e.g. EXPT_1. if not specified, set as ""
OUTPUT_TYPE_DATA = 'csv' # the output file type for the clean data files. Available options: 'csv', 'xlsx'. If not specified, default is 'csv'
OUTPUT_TYPE_DICT = 'xlsx' # the output file type fot the amended dictionary. Available options: 'csv', 'xlsx'. If not specified, default is 'xlsx'
