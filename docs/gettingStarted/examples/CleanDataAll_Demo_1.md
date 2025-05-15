---
layout: default
title: Example for CleanData class with All Cleaning Steps - Demo 1
parent: Examples
grand_parent: Getting Started
nav_order: 12
---

## Example of CleanData Class

This example demonstrates the use of the CleanData class to

- drop duplicate rows
- standardise text
- conversion of characters to ASCII-compatible format
- standardise dates
- exert constraints (Constraints class)

### Sample files used in this example

Users can refer to the provided sample files used in this demo:

- definitions: definitions_sample.py
- input data: sample_dataset.xlsx
- input data dictionary: sample_dataset_dict.xlsx
- main script: eg_cleanData_sample.py
- constraints script: eg_sample_constraints.py

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

Refer to the sample definitions.py (definitions_sample.py) provided for detailed guidance on individual attributes.

In addition to definitions.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.

In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:

- input data: sample_dataset.xlsx
- input data dictionary: sample_dataset_dict.xlsx

for a better idea of what a data dictionary comprises.

```
import definitions as defi
```

### INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS

When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.

Upon initialisation, the CleanData class automatically

- strips all leading/trailing empty spaces from variable names (optional), (default is False)
- checks if the variables given in the input data matches the meta information stored in the data dictionary.
- extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
- save the new input data and data dictionary files in the new folder
- computes an initial report, saved in the new folder

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

#### Indexing of rows in the initial report

As mentioned earlier, an initial report is automatically created when the CleanData class is initialized. The filename of the initial report is defined by the `INITIAL_REPORT_FILENAME` variable in the definitions_sample.py

The initial report identifies pre-cleaned data rows that may contain errors. By default, these rows are indexed based on the dataframe's default integer index, which is 0-based.
To ensure proper and meaningful indexing in the report, it is recommended to define the following variables in the definitions_sample.py:

- CREATE_UNIQUE_INDEX = True
- UNIQUE_INDEX_COMPOSITION_LIST = ["Name"]

The rows will now be indexed based on the UNIQUE_INDEX_COMPOSITION_LIST.

```
Initial Report Generated: filename: *\copula-tabular\examples\trainData\initial_report_sample.csv
```

### CLEAN THE DATA BY DROPPING DUPLICATE ROWS

In this example, we perform an additional adhoc operation to drop any duplicate rows found in the input data.

To do this, we specify the following global variables in the definitions_sample.py:

- OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME = 'rowsRemoved_sample.xlsx' # output file name to store the duplicated rows which have been dropped
- SUFFIX_DROPPED_DUPLICATED_ROWS = "DD" # suffix to append to the end of the latest output filename of the input data.

If there are unique 'index' variables in the input data, we may wish to tell the function to ignore these variables when checking duplication. 'Index' variables are unique for every row (not subject), and will confound the duplication checking process. We denote these variables using the 'CATEGORY' column of the data dictionary, and by setting its corresponding value to 'Index'. In this example (see sample_dataset_dict.xlsx), the variable 'ID' has the value 'Index' for its column 'ROWID'.

The cleaned input data is stored under a filename \*-`<SUFFIX_DROPPED_DUPLICATED_ROWS>`.xlsx.

```
cd.drop_duplicate_rows()
```

#### Dropped duplicate rows output

```
Dropping duplicate rows in input data...
No. of dropped rows: 10
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\sample_dataset-DD.csv
```

### CLEAN THE DATA BY STANDARDISING TEXT VARIABLES (CAPITAL/SMALL LETTERS)

In this example, we perform another adhoc operation to convert text/string variables into a standardise case (capital/small letters) format.

To do this, we specify the following global variables in the definitions_sample.py:

- OPTIONS_STANDARDISE_TEXT_CASE_TYPE = 'uppercase' # default case type to convert strings into: "uppercase", "lowercase", "capitalise"
- OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST = ["Name", "BMI_WHO"] # variables to exclude from the conversion.
- OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT = {"Gender": "lowercase"} # dictionary to customise case_type for specific variables, overwriting default

Note that 'index' variables are automatically excluded from this standardisation/conversion. Missing "string" type values will be converted to `<NA>`.

The cleaned input data is stored under a filename \*-`<SUFFIX_STANDARDISE_TEXT>`.xlsx.

```
cd.standardise_text()
```

#### Standardised text variables output

```
Standardising text in input data...
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\sample_dataset-DD-ST.csv
```

```
print(cd.clean_df)
```

```
ROWID  PID               Name  Gender  ...      BMI_WHO
    1    1      David Johnson    male  ... 25.0_to_29.9
    2    2        Anna Müller  female  ... 18.5_to_24.9
    7    5     Peter Phillips    male  ... 25.0_to_29.9
    8    6         José Silva    male  ... 25.0_to_29.9
    9    7      Marie Fischer  female  ... 25.0_to_29.9
   12    8        Björn Lopez    male  ... 18.5_to_24.9
   13    9       Søren Hansen    male  ... 25.0_to_29.9
   14   10   Nia Renée Miller  female  ... 25.0_to_29.9
   15   11        James Marie    male  ... 18.5_to_24.9
   16   12   Charlotte Carter  female  ... 25.0_to_29.9
   19   13   Laura San Martín  female  ...         <NA>
   20   14   Élisabeth Louise  female  ... 18.5_to_24.9
   22   15          Tom Davis    male  ... 18.5_to_24.9
   23   16         Émile Noël    male  ... 25.0_to_29.9
   25   17          Òrla Isla  female  ...         <NA>
   26   18       Amelia Grant  female  ...         <NA>
   27   19  David Lloyd Evans    male  ... 25.0_to_29.9
   29   20     Vittoria Rossi  female  ... 25.0_to_29.9
```

### CLEAN THE DATA WITH CONVERSION OF CHARACTERS

In this example, we perform another adhoc operation to convert characters to ASCII-compatible characters.

To do that, we specify the following global variables in the definitions_sample.py.

- SUFFIX_CONVERT_ASCII = 'ASCII'
- OPTIONS_CONVERT_ASCII_EXCLUSION_LIST = ['€','$','Ò'] # list of characters to exclude from conversion

```
cd.converting_ascii()
```

#### Converted ASCII-Compatible variables output

International accents have been removed from the variable `accents`, except for excluded characters ['€','$','Ò']

The output dataset has been saved in the trainData folder, with the `ASCII` suffix.

```
Converting all characters to ASCII-compatible in input data...
List of Exclusions:
['€', '$', 'Ò']
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\sample_dataset-DD-ST-ASCII.csv
```

```
print(cd.clean_df)
```

```
ROWID  PID           Name   Gender  ...   Total Care Cost
1    1      David Johnson     male  ...         $2200.50
2    2        Anna Muller   female  ...         €1360.42
4    3        Òscar Smith     male  ...         $2050.10
5    4     Maria Williams   female  ...         $2260.76
7    5     Peter Phillips     male  ...         $1705.00
8    6         Jose Silva     male  ...         $2485.76
9    7      Marie Fischer   female  ...         $2900.70
12    8        Bjorn Lopez    male  ...         $2660.33
13    9       Soren Hansen    male  ...         $1860.10
14   10   Nia Renee Miller  female  ...         $2306.40
15   11        James Marie    male  ...         $2570.96
16   12   Charlotte Carter  female  ...         $1560.60
19   13   Laura San Martin  female  ...         $1977.64
20   14   Elisabeth Louise  female  ...         $1250.20
22   15          Tom Davis    male  ...         $1782.70
23   16         Emile Noel    male  ...         $2610.95
25   17          Òrla Isla  female  ...         $2150.30
26   18       Amelia Grant  female  ...         €1600.36
27   19  David Lloyd Evans    male  ...         $1506.40
29   20     Vittoria Rossi  female  ...         €2053.08
```

### CLEAN THE DATA BY STANDARDISING DATES

In this example, we perform an additional adhoc operation to standardise the date formats for all `date` columns found in the input data.

To perform this operation, we need to indicate which are the columns that contain data that have been formatted as dates. We will do this using the data dictionary, which contains the metadata of the dataset. In our sample data dictionary, the variables `Date of Birth`, `Date of First Visit`, `Date of Diagnosis` and `Date of Treatment` are all dates. Therefore, under the `TYPE` column of the data dictionary, the data types of the three variables are indicated as `date`, instead of `numeric` or `string`.

Additional, under the `CODINGS` column, we may further specify the type of date format that variable has been coded in. For instance, `Date of First Visit` has been coded in the `mm/dd/yyyy` format.

Remember that we want to clean the data by standardising the date formats. To do that, we specify the following global variables in the definitions_sample.py.

- SUFFIX_STANDARDISE_DATE = 'DATE'
- OPTIONS_STANDARDISE_DATE_FORMAT = 'ddd, dd mmmm yy' # the standard date format to use for all dates (if not specified, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]
- OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME = 'failed_date_conversions_sample.csv' # file location for storing list of failed date conversions (only csv)

```
cd.standardise_date()
```

#### Standardised date variables output

In this example, multiple date variables are used to demonstrate how the format applied in MS EXCEL and the `CODINGS` specified in the dictionary can affect the reading and cleaning of date values:

|                Name | MS EXCEL FORMAT | CODINGS    | OUTPUT                                                                                                                             |
| ------------------: | :-------------- | :--------- | ---------------------------------------------------------------------------------------------------------------------------------- |
|       Date of Birth | CUSTOM (DATE)   |            | Correct. DATE format ensured that the data was read and converted correctly                                                        |
| Date of First Visit | DATE            | mm/dd/yyyy | Correct. DATE format preserved the data as a valid date, despite the wrong coding. The correct coding should have been yyyy-mm-dd. |
|   Date of Diagnosis | TEXT            |            | Correct. CleanData matched the data using common date formats and perform the conversion accordingly.                              |
|   Date of Treatment | TEXT            | mm-dd-yyyy | Some rows incorrect. The data could not be matched against the wrong coding. The correct coding should have been dd-mm-yyyy.       |

Print Original Dataset:

Note that MS Excel allows one to specify the data format of the cell. One might prefer to fix the data as the `Date` format, a style that has been replicated in variables `Date of Birth` and `Date of First Visit`. In this setup, dates can be automatically converted to its correct format, according to its specified MS EXCEL date format. Alternatively, one might encounter dates that are designated with the `Text` format. This situation is more complicated as its proper date format is not known. We replicated this situation in variables `Date of Diagnosis` and `Date of Treatment`.

```
print(cd.raw_df)
```

```
    ROWID  PID ...  Date of Birth Date of First Visit Date of Diagnosis Date of Treatment
    1    1     ...     2009-01-11          2019-04-13         19/4/2019         21-4-2019
    2    2     ...     1996-12-05          2019-02-11         20/2/2019         27-2-2019
    4    3     ...     2008-07-18          2020-03-29          3/4/2020         18-4-2020
    5    4     ...     1992-02-13          2019-07-15         30/7/2019          4-8-2020
    7    5     ...     2006-11-07          2022-04-26         17/5/2022         27-5-2022
    8    6     ...     1995-09-11          2020-06-19         28/6/2020          5-7-2020
   12    8     ...     1987-04-12          2020-10-29         5/11/2020         8-11-2020
   13    9     ...     1998-08-05          2021-05-12          1/6/2021         12-6-2021
   14   10     ...     2006-09-10          2019-02-19          2/3/2019         10-3-2019
   15   11     ...     1989-03-18          2021-04-30          7/5/2021         20-5-2021
   16   12     ...     2002-07-11          2022-02-28         12/3/2022         14-3-2022
   19   13     ...     1985-07-07          2021-12-15          4/1/2022          7-1-2022
   20   14     ...     2006-11-07          2021-01-29          8/2/2021         19-2-2021
   22   15     ...     2005-09-16          2022-09-02         17/9/2022         19-9-2022
   23   16     ...     1988-09-17          2022-04-01         12/4/2022         21-4-2022
   25   17     ...     2007-09-04          2021-07-04          1/8/2021         12-8-2021
   26   18     ...     1996-04-20          2022-09-12         19/9/2022        25-10-2022
   27   19     ...     1986-02-11          2022-10-16         2/11/2022        11-11-2022
   29   20     ...     2004-06-15          2022-11-03        25/11/2022         4-12-2022

```

Print Original Data Dictionary:

Notice that we have not specified `CODINGS` for the date variables `Date of Birth` and `Date of Diagnosis`. CleanData, nevertheless, tries to match the data to common date formats and perform the conversion accordingly. We have specified `CODINGS` for `Date of First Visit` and `Date of Treatment`, but have used the wrong format (`mm-dd-yyyy`) for `Date of Treatment`. The proper format should have been `dd-mm-yyyy`. The format for `Date of First Visit` is also wrong, but because we have used the `Date` format in MS Excel, the dates were still read correctly.

```
print(cd.dict_df)
```

```
                    NAME     TYPE      ...          CODINGS
...                  ...      ...      ...              ...
 11        Date of Birth     date      ...              NaN
 12  Date of First Visit     date      ...       mm/dd/yyyy
 13    Date of Diagnosis     date      ...              NaN
 14    Date of Treatment     date      ...       mm-dd-yyyy
```

Print Cleaned Data (with standardised dates):

We see that `Date of Birth`, `Date of First Visit` and `Date of Diagnosis` have been converted correctly into the required `ddd, dd mmmm yy` format. However `Date of Treatment` conversion has failed for certain entries, as CleanData tried to used the given `CODINGS`, which was wrong. When the conversion fails, possible mistakes will be stored in the file given under the name `OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME`.

The output dataset has been saved in the trainData folder, with the `DATE` suffix.

```
print(cd.clean_df)
```

```
ROWID  PID   ...        Date of Birth   Date of First Visit     Date of Diagnosis    Date of Treatment
    1    1   ...   Sun, 11 January 09      Sat, 13 April 19      Fri, 19 April 19                  NaN
    2    2   ...  Thu, 05 December 96   Mon, 11 February 19   Wed, 20 February 19                  NaN
    4    3   ...      Fri, 18 July 08      Sun, 29 March 20      Fri, 03 April 20                  NaN
    5    4   ...  Thu, 13 February 92       Mon, 15 July 19       Tue, 30 July 19     Wed, 08 April 20
    7    5   ...  Tue, 07 November 06      Tue, 26 April 22        Tue, 17 May 22                  NaN
    8    6   ...   Sun, 09 October 05       Thu, 28 July 22     Mon, 01 August 22     Fri, 08 April 22
    9    7   ... Mon, 11 September 95       Fri, 19 June 20       Sun, 28 June 20       Thu, 07 May 20
   12    8   ...     Sun, 12 April 87    Thu, 29 October 20   Thu, 05 November 20    Tue, 11 August 20
   13    9   ...    Wed, 05 August 98        Wed, 12 May 21       Tue, 01 June 21  Mon, 06 December 21
   14   10   ... Sun, 10 September 06   Tue, 19 February 19      Sat, 02 March 19   Thu, 03 October 19
   15   11   ...     Sat, 18 March 89      Fri, 30 April 21        Fri, 07 May 21                  NaN
   16   12   ...      Thu, 11 July 02   Mon, 28 February 22      Sat, 12 March 22                  NaN
   19   13   ...      Sun, 07 July 85   Wed, 15 December 21    Tue, 04 January 22      Fri, 01 July 22
   20   14   ...  Tue, 07 November 06    Fri, 29 January 21   Mon, 08 February 21                  NaN
   22   15   ... Fri, 16 September 05  Fri, 02 September 22  Sat, 17 September 22                  NaN
   23   16   ... Sat, 17 September 88      Fri, 01 April 22      Tue, 12 April 22                  NaN
   25   17   ... Tue, 04 September 07       Sun, 04 July 21     Sun, 01 August 21  Wed, 08 December 21
   26   18   ...     Sat, 20 April 96  Mon, 12 September 22  Mon, 19 September 22                  NaN
   27   19   ...  Tue, 11 February 86    Sun, 16 October 22   Wed, 02 November 22  Fri, 11 November 22
   29   20   ...      Tue, 15 June 04   Thu, 03 November 22   Fri, 25 November 22     Tue, 12 April

```

Print Updated Data Dictionary:

The data dictionary will be updated with the new date format, under `CODINGS`.

```
print(cd.clean_dict_df)
```

```
                    NAME     TYPE      ...          CODINGS
...                  ...      ...      ...              ...
 11        Date of Birth     date      ...   ddd, dd mmmm yy
 12  Date of First Visit     date      ...   ddd, dd mmmm yy
 13    Date of Diagnosis     date      ...   ddd, dd mmmm yy
 14    Date of Treatment     date      ...   ddd, dd mmmm yy
```

##### Sample output

The output dataset has been saved in the trainData folder, with the `DATE` suffix.

```
Standardising date/time in input data...
Standardise date: raw_dateCOlFieldFormat for variable Date of Diagnosis is not valid.
Using %d/%m/%Y as date format.
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\sample_dataset-DD-ST-ASCII-DATE.csv
```

### CLEAN THE DATA BY EXERTING CONSTRAINTS

In this example, we demonstrate the use of the CleanData class together with the Constraints class to exert constraints.

#### Import Libraries

```
# LOAD DEPENDENCIES
from bdarpack.Constraints import Constraints
```

eg_sample_constraints is a script where the constraints specific to the nhanes have been stored. They consists of functions which take in a dataframe from the CleanData class and an object of the Constraints class, and returns a constrained dataframe and an updated Constraints class that captured the details of the transformation.

```
import eg_sample_constraints as n_con
```

#### Use Constraints

Load the dataframe from the CleanData object. Initialise a new Constraints object.

```
con = Constraints(
    debug=True,
    logging=True, #whether to perform logging for constraints
    logger=cd.logger #use the same logfile as cleanData. If `None`, and `logging==True`, an additional `constraints_logfile.txt` file
                      containing only constraints-related logs will be created in the root folder.
)
```

The following are examples of constraints used on the variables of the sample dataset. The dataset undergoes a series of constraints, as stipulated by the metadata.

```
df, con = n_con.con_age(df, con)
df, con = n_con.con_ageMonths(df, con)
df, con = n_con.con_BMI(df, con, bmiChartPerc_filename=f"{cd.raw_data_path}bmiagerev.xls")
```

##### Sample output

```
Checking column: Age against Age_dup
Mismatched rows index: Björn Lopez_11,Amelia Grant_25
For variable: Age_dup: Replaced Age using conditions and values given in dict_conditions_values.
Checking column: AgeMonths against AgeMonths_dup
Mismatched rows index: Too many to show.
For variable: AgeMonths_dup: Replaced AgeMonths using conditions and values given in dict_conditions_values.
Checking column: BMI against BMI_dup
Columns are identical.
For variable: BMI_dup: Replaced BMI using conditions and values given in dict_conditions_values.
Checking column: BMICatUnder20yrs against BMICatUnder20yrs_dup
Mismatched rows index: Too many to show.
For variable: BMICatUnder20yrs_dup: Replaced BMICatUnder20yrs using conditions and values given in dict_conditions_values.
Checking column: BMI_WHO against BMI_WHO_dup
Mismatched rows index: José Silva_7,Charlotte Carter_15,Laura San Martín_18,Òrla Isla_24,Amelia Grant_25,David Lloyd Evans_26,Vittoria Rossi_28
For variable: BMI_WHO_dup: Replaced BMI_WHO using conditions and values given in dict_conditions_values.
```

#### Check Output

Check details of the constrained dataset

```
pprint.pprint(con.log)
```

#### Update CleanData class

Update the CleanData class with constrained data.

```
cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)
```

##### Sample Output

```
{'Age': {'evaluate_df_column': {'msg': 'Replaced Age using conditions and '
                                       'values given in '
                                       'dict_conditions_values.',
                                'replaced': 'Björn Lopez_11,Amelia Grant_25'}},
 'AgeMonths': {'evaluate_df_column': {'msg': 'Replaced AgeMonths using '
                                             'conditions and values given in '
                                             'dict_conditions_values.',
                                      'replaced': 'David Johnson_0,Anna '
                                                  'Müller_1,Òscar '
                                                  'Smith_3,Mária '
                                                  'Williams_4,Peter '
                                                  'Phillips_6,José '
                                                  'Silva_7,Marie '
                                                  'Fischer_8,Björn '
                                                  'Lopez_11,Søren '
                                                  'Hansen_12,Nia Renée '
                                                  'Miller_13,James '
                                                  'Marie_14,Charlotte '
                                                  'Carter_15,Laura San '
                                                  'Martín_18,Élisabeth '
                                                  'Louise_19,Tom '
                                                  'Davis_21,Émile Noël_22,Òrla '
                                                  'Isla_24,Amelia '
                                                  'Grant_25,David Lloyd '
                                                  'Evans_26,Vittoria '
                                                  'Rossi_28'}},
 'BMI': {'evaluate_df_column': {'msg': 'Replaced BMI using conditions and '
                                       'values given in '
                                       'dict_conditions_values.',
                                'replaced': 'No mismatches'}},
 'BMICatUnder20yrs': {'evaluate_df_column': {'msg': 'Replaced BMICatUnder20yrs '
                                                    'using conditions and '
                                                    'values given in '
                                                    'dict_conditions_values.',
                                             'replaced': 'David Johnson_0,Anna '
                                                         'Müller_1,Òscar '
                                                         'Smith_3,Mária '
                                                         'Williams_4,Peter '
                                                         'Phillips_6,José '
                                                         'Silva_7,Marie '
                                                         'Fischer_8,Björn '
                                                         'Lopez_11,Søren '
                                                         'Hansen_12,Nia Renée '
                                                         'Miller_13,James '
                                                         'Marie_14,Charlotte '
                                                         'Carter_15,Laura San '
                                                         'Martín_18,Élisabeth '
                                                         'Louise_19,Tom '
                                                         'Davis_21,Émile '
                                                         'Noël_22,Òrla '
                                                         'Isla_24,Amelia '
                                                         'Grant_25,David Lloyd '
                                                         'Evans_26,Vittoria '
                                                         'Rossi_28'}},
 'BMI_WHO': {'evaluate_df_column': {'msg': 'Replaced BMI_WHO using conditions '
                                           'and values given in '
                                           'dict_conditions_values.',
                                    'replaced': 'José Silva_7,Charlotte '
                                                'Carter_15,Laura San '
                                                'Martín_18,Òrla Isla_24,Amelia '
                                                'Grant_25,David Lloyd '
                                                'Evans_26,Vittoria Rossi_28'}}}
Replacing the input data...
Replacing the input data complete. new filename: *\copula-tabular\examples\trainData\sample_dataset-DD-ST-ASCII-DATE-CON.csv
```

### GENERATE REPORT AFTER CLEANING

You may generate a final report after the data cleaning is done.

The `report_filename` defaults to `INITIAL_REPORT_FILENAME` from definitions_sample.py. This will overwrite the initial report created during CleanData initialization.

It is recommended to provide a different name to preserve both initial and final reports. In this example, we have defined `report_filename="final_report_sample.xlsx"`.

```
cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df,report_filename="final_report_sample.xlsx")
print(cd.report_df)
```

#### Sample Output

The final report identifies post-cleaned data rows that may contain errors.
We have earlier defined the following variables in the definitions_sample.py to ensure proper and meaningful indexing in the report:

- CREATE_UNIQUE_INDEX = True
- UNIQUE_INDEX_COMPOSITION_LIST = ["Name"]

```
Initial Report Generated: filename: *\copula-tabular\examples\trainData\final_report_sample.xlsx
```

```
print(cd.report_df)
```

```
                    data_type data_type_in_dict  ... numeric_range_error_list                                str_list_error_list
ROWID                   Int64           numeric  ...                     N.A.                                               N.A.
PID                     Int64           numeric  ...                     N.A.                                               N.A.
Name                   string            string  ...                     N.A.                                               N.A.
Gender                 string            string  ...                     N.A.                                               N.A.
Age                     Int64           numeric  ...                     N.A.                                               N.A.
AgeMonths               Int64           numeric  ...                     N.A.                                               N.A.
Height                Float64           numeric  ...     David Lloyd Evans_26                                               N.A.
Weight                Float64           numeric  ...        Vittoria Rossi_28                                               N.A.
BMI                   Float64           numeric  ...                     N.A.                                               N.A.
BMICatUnder20yrs       string            string  ...                     N.A.  Anna Müller_1,Mária Williams_4,Marie Fischer_8...
BMI_WHO                string            string  ...                     N.A.   Laura San Martín_18,Òrla Isla_24,Amelia Grant_25
Date of Birth          object              date  ...                     N.A.                                               N.A.
Date of First Visit    object              date  ...                     N.A.                                               N.A.
Date of Diagnosis      object              date  ...                     N.A.                                               N.A.
Date of Treatment      object              date  ...                     N.A.                                               N.A.
Total Care Cost        string            string  ...                     N.A.                                               N.A.
```
