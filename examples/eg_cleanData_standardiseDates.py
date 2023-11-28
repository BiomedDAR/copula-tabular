# This example demonstrates the use of the CleanData class to 
# - standardise dates
# - conversion of characters to ASCII-compatible format

# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.CleanData import CleanData

# LOAD DEFINITIONS
# The definitions.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined.
# Refer to the sample definitions_date.py provided for detailed guidance on individual attributes required for date standardisation.
# In addition to definitions.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.
# In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:
    # -- input data: date_dataset.xlsx
    # -- input data dictionary: date_dataset_dict.xlsx
# for a better idea of what a data dictionary comprises.

import definitions_date as defi

# INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS
# When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.
# Upon initialisation, the CleanData class automatically 
# -- strips all leading/trailing empty spaces from variable names (optional), (default is False)
# -- checks if the variables given in the input data matches the meta information stored in the data dictionary.
# -- extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
# -- save the new input data and data dictionary files in the new folder

cd = CleanData(definitions=defi)

# CLEAN THE DATA BY STANDARDISING DATES
# In this example, we perform an additional adhoc operation to standardise the date formats for all 'date' columns found in the input data.
# To perform this operation, we need to indicate which are the columns that contain data that have been formatted as dates. We will do this using the data dictionary, which contains the metadata of the dataset. In our sample data dictionary, the variables 'date_1', 'date_2', and 'date_3' are all dates. Therefore, under the "TYPE" column of the data dictionary, the data types of the three variables are indicated as 'date', instead of 'numeric' or 'string'.
# Additional, under the "CODINGS" column, we may further specify the type of date format that variable has been coded in. For instance, 'date_2' has been coded in the 'mm/dd/yyyy' format.
# Remember that we want to clean the data by standardising the date formats. To do that, we specify the following global variables in the definitions_date.py.
#  -- SUFFIX_STANDARDISE_DATE = 'DATE'
#  -- OPTIONS_STANDARDISE_DATE_FORMAT = 'ddd, dd mmmm yy' # the standard date format to use for all dates (if not specified, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]
#  -- OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME = 'failed_date_conversions.csv' # file location for storing list of failed date conversions (only csv)

cd.standardise_date()

# PRINT ORIGINAL DATASET
print(cd.raw_df)
# Note that MS Excel allows one to specific the data format of the cell. One might prefer to fix the data as the 'Date' format, a style that has been replicated in variables 'date_1' and 'date_2'. In this setup, dates can be automatically converted to its correct yyyy-mm-dd format, according to its specified MS EXCEL date format. Alternatively, one might encounter dates that are designated with the 'Custom' or 'Text' format. This situation is more complicated as its proper date format is not known. We replicated this situation in variables 'date_3' and 'date_4.

# PRINT ORIGINAL DATA DICTIONARY
# Notice that we have not specified "CODINGS" for the date variables 'date_1' and 'date_3'. CleanData, nevertheless, tries to match the data to common date formats and perform the conversion accordingly. We have specified "CODINGS" for 'date_1' and 'date_4', but have used the wrong one (mm-dd-yyyy) for date_4. The proper one should have been 'dd-mm-yyyy'.
print(cd.dict_df)

# PRINT CLEAN DF (WITH STANDARDISED DATES)
print(cd.clean_df)
# We see that 'date_1' to 'date_3' have been converted correctly into the required 'ddd, dd mmmm yy' format. However 'date_4' conversion has failed for certain entries, as CleanData tried to used the given "CODINGS", which was wrong. When the conversion fails, possible mistakes will be stored in the file given under the name OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME.
# The output dataset has been saved in the trainData folder, with the 'DATE' suffix.

# PRINT UPDATED DATA DICTIONARY
# The data dictionary will be updated with the new date format, under "CODINGS".
print(cd.clean_dict_df)


# CONVERSION OF CHARACTERS
# In this example, we perform an additional adhoc operation to convert characters to ASCII-compatible characters.
# To do that, we specify the following global variables in the definitions_date.py.
#  -- SUFFIX_CONVERT_ASCII = 'ASCII'
#  -- OPTIONS_CONVERT_ASCII_EXCLUSION_LIST = ['€','$','Ò'] # list of characters to exclude from conversion
cd.converting_ascii()

# PRINT CLEAN DF (CONVERTED CHARACTERS)
# International accents have been removed from the variable 'accents', except for excluded characters ['€','Ò']
# The output dataset has been saved in the trainData folder, with the 'ASCII' suffix.
print(cd.clean_df)