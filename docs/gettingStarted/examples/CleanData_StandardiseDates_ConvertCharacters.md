---
layout: default
title: Example for CleanData class (Date Standardisation, Character Conversion)
parent: Examples
grand_parent: Getting Started
nav_order: 5
---

## Example of CleanData Class
This example demonstrates the use of the CleanData class to
*   standardise dates
*   conversion of characters to ASCII-compatible format

### Import Libraries
```
# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from mz.CleanData import CleanData
```

### Import Definitions
The definitions.py is where most, if not all, of the global attributes in the tabular-copula pipeline are defined.

Refer to the sample definitions_date.py provided for detailed guidance on individual attributes required for date standardisation.

In addition to definitions.py, the CleanData class also requires a proper data dictionary that includes meta information on the variables one expects to see in the input data file.

In this example, the folder name for all raw data files is specified as RAW_PATH="rawData". Users can refer to the provided sample files:

*   input data: date_dataset.xlsx
*   input data dictionary: date_dataset_dict.xlsx

for a better idea of what a data dictionary comprises.
```
import definitions_date as defi
```

### INITIALISE THE CLEANDATA CLASS WITH LOADED DEFINITIONS
When the CleanData class is initialised, it automatically reads the input data and data dictionary files as defined in the definitions.py. It then generates a new folder in the root directory--the name of this folder can be specified in definitions.py--and stores all the outputs of its assigned cleaning tasks in this folder.

Upon initialisation, the CleanData class automatically 

*   strips all leading/trailing empty spaces from variable names (optional), (default is False)
*   checks if the variables given in the input data matches the meta information stored in the data dictionary.
*   extracts a list of longitudinal markers (ignore if there are no longitudinal markers specified)
*   save the new input data and data dictionary files in the new folder

```
cd = CleanData(definitions=defi)
```

### CLEAN THE DATA BY STANDARDISING DATES
In this example, we perform an additional adhoc operation to standardise the date formats for all `date` columns found in the input data.

To perform this operation, we need to indicate which are the columns that contain data that have been formatted as dates. We will do this using the data dictionary, which contains the metadata of the dataset. In our sample data dictionary, the variables `date_1`, `date_2`, and `date_3` are all dates. Therefore, under the `TYPE` column of the data dictionary, the data types of the three variables are indicated as `date`, instead of `numeric` or `string`.

Additional, under the `CODINGS` column, we may further specify the type of date format that variable has been coded in. For instance, `date_2` has been coded in the `mm/dd/yyyy` format.

Remember that we want to clean the data by standardising the date formats. To do that, we specify the following global variables in the definitions_date.py.
*   SUFFIX_STANDARDISE_DATE = 'DATE'
*   OPTIONS_STANDARDISE_DATE_FORMAT = 'ddd, dd mmmm yy' # the standard date format to use for all dates (if not specified, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]
*   OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME = 'failed_date_conversions.csv' # file location for storing list of failed date conversions (only csv)

```
cd.standardise_date()
```

#### Standardised date variables output

Print Original Dataset:

Note that MS Excel allows one to specific the data format of the cell. One might prefer to fix the data as the `Date` format, a style that has been replicated in variables `date_1` and `date_2`. In this setup, dates can be automatically converted to its correct `yyyy-mm-dd` format, according to its specified MS EXCEL date format. Alternatively, one might encounter dates that are designated with the `Custom` or `Text` format. This situation is more complicated as its proper date format is not known. We replicated this situation in variables `date_3` and `date_4`.

```
print(cd.raw_df)
```

```
    ID     date_1     date_2       date_3      date_4            accents
0    1 2009-01-11 1989-04-13     9/5/1995   11-1-2009              ÂéüÒÑ
1    2 1985-12-05 2007-04-11    20/4/2009   5-12-1985              ÂéüÒÑ
2    3 2008-07-18 2000-03-02   15/11/1982   18-7-2008              ÂéüÒÑ
3    4 1992-07-23 2009-04-15   10/10/1995   23-7-1992              ÂéüÒÑ
4    5 2006-11-07 2003-04-26    17/6/1998   7-11-2006             ÂéüÒÑÂ
5    6 2000-10-09 2003-07-28    30/7/1996   9-10-2000  ÂéüÒÑ€ȁȂȃȄȅȧȫȮȯȞȲ
6    7 1995-09-11 1984-06-19    16/2/2009   11-9-1995              ÂéüÒÑ
7    8 1987-08-06 1987-10-29     5/8/1989    6-8-1987              ÂéüÒÑ
8    9 1995-08-25 2006-05-12    31/7/1983   25-8-1995              ÂéüÒÑ
9   10 1995-09-27 1999-02-19     1/9/1992   27-9-1995              ÂéüÒÑ
10  11 1989-03-21 1985-04-30    7/10/1984   21-3-1989              ÂéüÒÑ
11  12 2004-07-11 1986-02-28    12/4/2004   11-7-2004              ÂéüÒÑ
12  13 1985-07-07 1998-12-05     9/2/1991    7-7-1985              ÂéüÒÑ
13  14 2004-11-07 1996-01-27     3/3/1984   7-11-2004              ÂéüÒÑ
14  15 2005-09-16 1987-09-02    17/9/1985   16-9-2005              ÂéüÒÑ
15  16 1988-09-17 1998-04-01    8/12/1996   17-9-1988              ÂéüÒÑ
```

Print Original Data Dictionary

Notice that we have not specified `CODINGS` for the date variables `date_1` and `date_3`. CleanData, nevertheless, tries to match the data to common date formats and perform the conversion accordingly. We have specified `CODINGS` for `date_1` and `date_4`, but have used the wrong format (`mm-dd-yyyy`) for date_4. The proper format should have been `dd-mm-yyyy`.

```
print(cd.dict_df)
```

```
      NAME           DESCRIPTION     TYPE     CODINGS CATEGORY  COLUMN_NUMBER  SECONDARY  CONSTRAINTS
0       ID                   NaN  numeric         NaN    Index            NaN        NaN          NaN
1   date_1    Test Date Format 1     date         NaN     cat0            1.0        NaN          NaN
2   date_2    Test Date Format 2     date  mm/dd/yyyy     cat0            2.0        NaN          NaN
3   date_3    Test Date Format 3     date         NaN     cat0            3.0        NaN          NaN
4   date_4    Test Date Format 4     date  mm-dd-yyyy      NaN            NaN        NaN          NaN
5  accents  Data full of accents   string         NaN     cat1            4.0        NaN          NaN
```

Print Cleaned Data (with standardised dates)

We see that `date_1` to `date_3` have been converted correctly into the required `ddd, dd mmmm yy` format. However `date_4` conversion has failed for certain entries, as CleanData tried to used the given `CODINGS`, which was wrong. When the conversion fails, possible mistakes will be stored in the file given under the name `OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME`.

The output dataset has been saved in the trainData folder, with the `DATE` suffix.

```
print(cd.clean_df)
```

```
    ID                 date_1                 date_2                 date_3                 date_4            accents
0    1     Sun, 11 January 09       Thu, 13 April 89         Tue, 09 May 95    Sun, 01 November 09              ÂéüÒÑ
1    2    Thu, 05 December 85       Wed, 11 April 07       Mon, 20 April 09         Sun, 12 May 85              ÂéüÒÑ
2    3        Fri, 18 July 08       Thu, 02 March 00    Mon, 15 November 82                    nan              ÂéüÒÑ
3    4        Thu, 23 July 92       Wed, 15 April 09     Tue, 10 October 95                    nan              ÂéüÒÑ
4    5    Tue, 07 November 06       Sat, 26 April 03        Wed, 17 June 98        Tue, 11 July 06             ÂéüÒÑÂ
5    6     Mon, 09 October 00        Mon, 28 July 03        Tue, 30 July 96   Sun, 10 September 00  ÂéüÒÑ€ȁȂȃȄȅȧȫȮȯȞȲ
6    7   Mon, 11 September 95        Tue, 19 June 84    Mon, 16 February 09    Thu, 09 November 95              ÂéüÒÑ
7    8      Thu, 06 August 87     Thu, 29 October 87      Sat, 05 August 89        Mon, 08 June 87              ÂéüÒÑ
8    9      Fri, 25 August 95         Fri, 12 May 06        Sun, 31 July 83                    nan              ÂéüÒÑ
9   10   Wed, 27 September 95    Fri, 19 February 99   Tue, 01 September 92                    nan              ÂéüÒÑ
10  11       Tue, 21 March 89       Tue, 30 April 85     Sun, 07 October 84                    nan              ÂéüÒÑ
11  12        Sun, 11 July 04    Fri, 28 February 86       Mon, 12 April 04    Sun, 07 November 04              ÂéüÒÑ
12  13        Sun, 07 July 85    Sat, 05 December 98    Sat, 09 February 91        Sun, 07 July 85              ÂéüÒÑ
13  14    Sun, 07 November 04     Sat, 27 January 96       Sat, 03 March 84        Sun, 11 July 04              ÂéüÒÑ
14  15   Fri, 16 September 05   Wed, 02 September 87   Tue, 17 September 85                    nan              ÂéüÒÑ
15  16   Sat, 17 September 88       Wed, 01 April 98    Sun, 08 December 96                    nan              ÂéüÒÑ
```

Print Updated Data Dictionary

The data dictionary will be updated with the new date format, under `CODINGS`.

```
print(cd.clean_dict_df)
```

```
      NAME           DESCRIPTION     TYPE          CODINGS CATEGORY  COLUMN_NUMBER  SECONDARY  CONSTRAINTS
0       ID                   NaN  numeric              NaN    Index            NaN        NaN          NaN
1   date_1    Test Date Format 1     date  ddd, dd mmmm yy     cat0            1.0        NaN          NaN
2   date_2    Test Date Format 2     date  ddd, dd mmmm yy     cat0            2.0        NaN          NaN
3   date_3    Test Date Format 3     date  ddd, dd mmmm yy     cat0            3.0        NaN          NaN
4   date_4    Test Date Format 4     date  ddd, dd mmmm yy      NaN            NaN        NaN          NaN
5  accents  Data full of accents   string              NaN     cat1            4.0        NaN          NaN
```



### CLEAN THE DATA WITH CONVERSION OF CHARACTERS
In this example, we perform an additional adhoc operation to convert characters to ASCII-compatible characters.

To do that, we specify the following global variables in the definitions_date.py.
*   SUFFIX_CONVERT_ASCII = 'ASCII'
*   OPTIONS_CONVERT_ASCII_EXCLUSION_LIST = ['€','$','Ò'] # list of characters to exclude from conversion

```
cd.converting_ascii()
```

#### Converted ASCII-Compatible variables output

International accents have been removed from the variable `accents`, except for excluded characters ['€','Ò']

The output dataset has been saved in the trainData folder, with the `ASCII` suffix.

```
print(cd.clean_df)
```

```
    ID                 date_1                 date_2                 date_3                 date_4            accents
0    1     Sun, 11 January 09       Thu, 13 April 89         Tue, 09 May 95    Sun, 01 November 09              AeuÒN
1    2    Thu, 05 December 85       Wed, 11 April 07       Mon, 20 April 09         Sun, 12 May 85              AeuÒN
2    3        Fri, 18 July 08       Thu, 02 March 00    Mon, 15 November 82                    nan              AeuÒN
3    4        Thu, 23 July 92       Wed, 15 April 09     Tue, 10 October 95                    nan              AeuÒN
4    5    Tue, 07 November 06       Sat, 26 April 03        Wed, 17 June 98        Tue, 11 July 06             AeuÒNA
5    6     Mon, 09 October 00        Mon, 28 July 03        Tue, 30 July 96   Sun, 10 September 00  AeuÒN€aAaEeaoOoHY
6    7   Mon, 11 September 95        Tue, 19 June 84    Mon, 16 February 09    Thu, 09 November 95              AeuÒN
7    8      Thu, 06 August 87     Thu, 29 October 87      Sat, 05 August 89        Mon, 08 June 87              AeuÒN
8    9      Fri, 25 August 95         Fri, 12 May 06        Sun, 31 July 83                    nan              AeuÒN
9   10   Wed, 27 September 95    Fri, 19 February 99   Tue, 01 September 92                    nan              AeuÒN
10  11       Tue, 21 March 89       Tue, 30 April 85     Sun, 07 October 84                    nan              AeuÒN
11  12        Sun, 11 July 04    Fri, 28 February 86       Mon, 12 April 04    Sun, 07 November 04              AeuÒN
12  13        Sun, 07 July 85    Sat, 05 December 98    Sat, 09 February 91        Sun, 07 July 85              AeuÒN
13  14    Sun, 07 November 04     Sat, 27 January 96       Sat, 03 March 84        Sun, 11 July 04              AeuÒN
14  15   Fri, 16 September 05   Wed, 02 September 87   Tue, 17 September 85                    nan              AeuÒN
15  16   Sat, 17 September 88       Wed, 01 April 98    Sun, 08 December 96                    nan              AeuÒN
```