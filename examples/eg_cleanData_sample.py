# This example demonstrates the use of the CleanData class.

# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.CleanData import CleanData

# LOAD DEFINITIONS
# The definitions_*.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined.
# Refer to the sample definitions_sample.py provided for detailed guidance on individual attributes.
# In addition to definitions_*.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.
# In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:
    # -- input data: sample_dataset.xlsx
    # -- input data dictionary: sample_dataset_dict.xlsx
# for a better idea of what a data dictionary comprises.

import definitions_sample as defi

# INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS
# When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.
# Upon initialisation, the CleanData class automatically 
# -- strips all leading/trailing empty spaces from variable names (optional), (default is False)
# -- checks if the variables given in the input data matches the meta information stored in the data dictionary.
# -- extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
# -- save the new input data and data dictionary files in the new folder
# -- computes an initial report, saved in the new folder

cd = CleanData(definitions=defi)

# PRINT INITIAL REPORT
# After the CleanData class is initialized, you may print an initial report.
# The initial report identifies pre-cleaned data rows that may contain errors.
print(cd.report_df)

# PRINT THE INITIAL DATAFRAME
# After the CleanData class is initialized, you may print the initial data to check that it is loaded properly
print(cd.raw_df)

# CLEAN THE DATA BY DROPPING DUPLICATE ROWS
# In this example, we perform an additional adhoc operation to drop any duplicate rows found in the input data.
# To do this, we specify the following global variables in the definitions.py:
#  -- OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME = 'rowsRemoved.xlsx' # output file name to store the duplicated rows which have been dropped
#  -- SUFFIX_DROPPED_DUPLICATED_ROWS = "DD" # suffix to append to the end of the output filename of the input data.
# If there are unique 'index' variables in the input data, we may wish to tell the function to ignore these variables when checking duplication. 'Index' variables are unique for every row (not subject), and will confound the duplication checking process. We denote these variables using the 'CATEGORY' column of the data dictionary, and by setting its corresponding value to 'Index'. In this example (see sample_dataset_dict.xlsx), the variable 'ID' has the value 'Index' for its column 'CATEGORY'.
# The cleaned input data is stored under a filename *-<SUFFIX_DROPPED_DUPLICATED_ROWS>.xlsx.
cd.drop_duplicate_rows()

# CLEAN THE DATA BY STANDARDISING TEXT VARIABLES (CAPITAL/SMALL LETTERS)
# In this example, we perform yet another adhoc operation to convert text/string variables into a standardise case (capital/small letters) format.
# To do this, we specify the following global variables in the definitions.py:
#  -- OPTIONS_STANDARDISE_TEXT_CASE_TYPE = 'uppercase' # default case type to convert strings into: "uppercase", "lowercase", "capitalise"
#  -- OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST = ["Gender", "Work"] # variables to exclude from the conversion.
#  -- OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT = {"Race1": "capitalise"} # dictionary to customise case_type for specific variables, overwriting default
# Note that 'index' variables are automatically excluded from this standardisation/conversion. Missing "string" type values will be converted to <NA>.
# The cleaned input data is stored under a filename *-<SUFFIX_STANDARDISE_TEXT>.xlsx.
cd.standardise_text()


# CONVERSION OF CHARACTERS
# In this example, we perform an additional adhoc operation to convert characters to ASCII-compatible characters.
# To do that, we specify the following global variables in the definitions_date.py.
#  -- SUFFIX_CONVERT_ASCII = 'ASCII'
#  -- OPTIONS_CONVERT_ASCII_EXCLUSION_LIST = ['€','$','Ò'] # list of characters to exclude from conversion
cd.converting_ascii()


# CLEAN THE DATA BY STANDARDISING DATES
# In this example, we perform an additional adhoc operation to standardise the date formats for all 'date' columns found in the input data.
# To perform this operation, we need to indicate which are the columns that contain data that have been formatted as dates. We will do this using the data dictionary, which contains the metadata of the dataset. In our sample data dictionary, the variables 'Date of Birth', 'Date of First Visit', 'Date of Diagnosis' and 'Date of Treatment' are all dates. Therefore, under the "TYPE" column of the data dictionary, the data types of the four variables are indicated as 'date', instead of 'numeric' or 'string'.
# Additional, under the "CODINGS" column, we may further specify the type of date format that variable has been coded in. For instance, 'date_2' has been coded in the 'mm/dd/yyyy' format.
# Remember that we want to clean the data by standardising the date formats. To do that, we specify the following global variables in the definitions_date.py.
#  -- SUFFIX_STANDARDISE_DATE = 'DATE'
#  -- OPTIONS_STANDARDISE_DATE_FORMAT = 'ddd, dd mmmm yy' # the standard date format to use for all dates (if not specified, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]
#  -- OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME = 'failed_date_conversions.csv' # file location for storing list of failed date conversions (only csv)

cd.standardise_date()

# LOAD DEPENDENCIES
from bdarpack.Constraints import Constraints

# eg_sample_constraints is a script where the constraints specific to the dataset sample_dataset.xlsx have been stored. They consists of functions which take in a dataframe from the CleanData class and an object of the Constraints class, and returns a constrained dataframe and an updated Constraints class that captured the details of the transformation.
import eg_sample_constraints as n_con

# USE CONSTRAINTS
df = cd.clean_df
con = Constraints(
    debug=True,
    logging=True, #whether to perform logging for constraints
    logger=cd.logger #use same logfile as cleanData. If None, new logfile will be created in root
)

# The following are examples of constraints used on the variables of the sample dataset.
df, con = n_con.con_age(df, con)
df, con = n_con.con_ageMonths(df, con)
df, con = n_con.con_BMI(df, con, bmiChartPerc_filename=f"{cd.raw_data_path}bmiagerev.xls")

# Check details of the constrained dataset
pprint.pprint(con.log)

# Output log variable to file
con.output_log_to_file()

# UPDATE CLEANDATA CLASS
# Update the CleanData class with constrained data
# The cleaned input data is stored under a filename *-<SUFFIX_CONSTRAINTS>.xlsx.

cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)

# PRINT FINAL REPORT
# The final report identifies post-cleaned data rows that may contain errors.
cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df,report_filename="final_report_sample.xlsx")
print(cd.report_df)