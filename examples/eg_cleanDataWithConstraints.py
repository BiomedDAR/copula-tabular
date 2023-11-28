# This example demonstrates the use of the CleanData class together with the Constraints class.

# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.CleanData import CleanData

# LOAD DEFINITIONS
# The definitions.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined.
# Refer to the sample definitions.py provided for detailed guidance on individual attributes.
# In addition to definitions.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.
# In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:
    # -- input data: nhanes_raw.xlsx
    # -- input data dictionary: nhanes_dict_2-1.xlsx
# for a better idea of what a data dictionary comprises.

import definitions as defi

# INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS
# When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.
# Upon initialisation, the CleanData class automatically 
# -- strips all leading/trailing empty spaces from variable names (optional), (default is False)
# -- checks if the variables given in the input data matches the meta information stored in the data dictionary.
# -- extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
# -- save the new input data and data dictionary files in the new folder

cd = CleanData(definitions=defi)

# CLEAN THE DATA BY DROPPING DUPLICATE ROWS
# In this example, we perform an additional adhoc operation to drop any duplicate rows found in the input data.
# To do this, we specify the following global variables in the definitions.py:
#  -- OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME = 'rowsRemoved.xlsx' # output file name to store the duplicated rows which have been dropped
#  -- SUFFIX_DROPPED_DUPLICATED_ROWS = "DD" # suffix to append to the end of the output filename of the input data.
# If there are unique 'index' variables in the input data, we may wish to tell the function to ignore these variables when checking duplication. 'Index' variables are unique for every row (not subject), and will confound the duplication checking process. We denote these variables using the 'CATEGORY' column of the data dictionary, and by setting its corresponding value to 'Index'. In this example (see nhanes_dict_2-1.xlsx), the variable 'ID' has the value 'Index' for its column 'CATEGORY'.
# The cleaned input data is stored under a filename *-<SUFFIX_DROPPED_DUPLICATED_ROWS>.xlsx.
cd.drop_duplicate_rows()

# PRINT REPORT
print(cd.report_df)

# LOAD DEPENDENCIES
from bdarpack.Constraints import Constraints

# eg_nhanes_constraints is a script where the constraints specific to the nhanes have been stored. They consists of functions which take in a dataframe from the CleanData class and an object of the Constraints class, and returns a constrained dataframe and an updated Constraints class that captured the details of the transformation.
import eg_nhanes_constraints as n_con

# USE CONSTRAINTS
df = cd.clean_df
con = Constraints(
    debug=True,
    logging=True, #whether to perform logging for constraints
    logger=cd.logger #use same logfile as cleanData. If None, new logfile will be created in root
)

# The following are examples of constraints used on the variables of the NHANES dataset.
df, con = n_con.con_ageDecade(df, con)
df, con = n_con.con_ageMonths(df, con)
df, con = n_con.con_Race3(df, con)
df, con = n_con.con_GenderEducationMaritalStatus(df, con)
df, con = n_con.con_HHIncome(df, con)
df, con = n_con.con_HomeWork(df, con)
df, con = n_con.con_WeightHeight(df, con)
df, con = n_con.con_BMI(df, con, bmiChartPerc_filename=f"{cd.raw_data_path}bmiagerev.xls")
df, con = n_con.con_Testosterone(df, con)
df, con = n_con.con_cholUrine(df, con)
df, con = n_con.con_diabetes(df, con)
df, con = n_con.con_HealthGen(df, con)
df, con = n_con.con_Depression(df, con)
df, con = n_con.con_Pregnancies(df, con)
df, con = n_con.con_Activeness(df, con)
df, con = n_con.con_Activity(df, con)
df, con = n_con.con_Alcohol(df, con)
df, con = n_con.con_Smoking(df, con)
df, con = n_con.con_Drugs(df, con)
df, con = n_con.con_Sex(df, con)
df, con = n_con.con_Pregnancies_2(df, con)

# Check details of the constrained dataset
pprint.pprint(con.log)

# Output log variable to file
con.output_log_to_file()

# UPDATE CLEANDATA CLASS
# Update the CleanData class with constrained data
# The cleaned input data is stored under a filename *-<SUFFIX_CONSTRAINTS>.xlsx.

cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)

# PRINT REPORT
cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df)
print(cd.report_df)