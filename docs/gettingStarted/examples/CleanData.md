---
layout: default
title: Example for CleanData class
parent: Examples
grand_parent: Getting Started
nav_order: 2
---

## Example of CleanData Class
This example demonstrates the use of the CleanData class.

### Import Libraries
```
# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.CleanData import CleanData
```

### Import Definitions
The definitions.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined.

Refer to the sample definitions.py provided for detailed guidance on individual attributes.

In addition to definitions.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.

In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:

*   input data: nhanes_raw.xlsx
*   input data dictionary: nhanes_dict_2-1.xlsx

for a better idea of what a data dictionary comprises.
```
import definitions as defi
```

### INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS
When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.

Upon initialisation, the CleanData class automatically 

*   strips all leading/trailing empty spaces from variable names (optional), (default is False)
*   checks if the variables given in the input data matches the meta information stored in the data dictionary.
*   extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
*   save the new input data and data dictionary files in the new folder
*   computes an initial report, saved in the new folder

```
cd = CleanData(definitions=defi)
```

#### Variable Mismatch Output
Suppose the input variable `TESTID` has been misspelt as `TESTid` in the data dictionary. The initialisation will throw an error, along with a list of mismatched variables:
```
There is a mismatch in the variable names extracted from the input data and the data dictionary. Use cleanData.var_diff_list to extract list of mismatched variable names.
Mismatched Variables:
 {'TESTid', 'TESTID'}
```

If there is no mismatches, the initialisation continues, with the following message:
```
No variable name mismatches found. Proceeding with next step of initialisation...
```

### CLEAN THE DATA BY DROPPING DUPLICATE ROWS
In this example, we perform an additional adhoc operation to drop any duplicate rows found in the input data.

To do this, we specify the following global variables in the definitions.py:

*   OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME = 'rowsRemoved.xlsx' # output file name to store the duplicated rows which have been dropped
*   SUFFIX_DROPPED_DUPLICATED_ROWS = "DD" # suffix to append to the end of the latest output filename of the input data.

If there are unique 'index' variables in the input data, we may wish to tell the function to ignore these variables when checking duplication. 'Index' variables are unique for every row (not subject), and will confound the duplication checking process. We denote these variables using the 'CATEGORY' column of the data dictionary, and by setting its corresponding value to 'Index'. In this example (see nhanes_dict_2-1.xlsx), the variable 'ID' has the value 'Index' for its column 'CATEGORY'.

The cleaned input data is stored under a filename *-`<SUFFIX_DROPPED_DUPLICATED_ROWS>`.xlsx.

```
cd.drop_duplicate_rows()
```

#### Dropped duplicate rows output
```
Dropping duplicate rows in input data...
No. of dropped rows: 2168
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\nhanes_raw-DD.csv
```

### CLEAN THE DATA BY STANDARDISING TEXT VARIABLES (CAPITAL/SMALL LETTERS)
In this example, we perform yet another adhoc operation to convert text/string variables into a standardise case (capital/small letters) format.

To do this, we specify the following global variables in the definitions.py:

*   OPTIONS_STANDARDISE_TEXT_CASE_TYPE = 'uppercase' # default case type to convert strings into: "uppercase", "lowercase", "capitalise"
*   OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST = ["Gender", "Work"] # variables to exclude from the conversion.
*   OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT = {"Race1": "capitalise"} # dictionary to customise case_type for specific variables, overwriting default

Note that 'index' variables are automatically excluded from this standardisation/conversion. Missing "string" type values will be converted to `<NA>`.

The cleaned input data is stored under a filename *-`<SUFFIX_STANDARDISE_TEXT>`.xlsx.
```
cd.standardise_text()
```

#### Standardised text variables output
```
Standardising text in input data...
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\nhanes_raw-DD-ST.csv
```