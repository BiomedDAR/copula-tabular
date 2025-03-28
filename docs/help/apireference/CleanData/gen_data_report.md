---
layout: default
title: Generate Data Report
parent: Clean Data
grand_parent: API Reference
nav_order: 2
---

# CleanData.gen_data_report

**CleanData.gen_data_report(*data*, *dict*, [*report_filename* ])**

Generates a report of `data`. Report include details such as
*   data_type
*   data_type_in_dict
*   data_type_mismatch
*   count_missing_values
*   percentage_missing_values
*   numeric_range
*   unique_categories

**Parameters**
- *data*: (dataframe)
  - data for which the report is to be generated
- *dict*: (dataframe)
  - dictionary for corresponding data
- *report_filename*: (string, optional)
  - optional `filename.xlsx` for storing report; provides an alternative to default option: `CleanData.initial_report_filename`. Output will be stored in the `CleanData.train_data_path` folder.

**Returns**
- *INT*
  - returns `1` if successfully saved to file, `0` otherwise

### Notes

*   currently, an initial report is automatically generated upon class initialisation.
*   report is saved to path: `CleanData.initial_report_filename`. Filepath can be set using `dictionary.py`
*   report is also saved as a dataframe as `CleanData.report_df`
*   an unfortunate consequence is that using `CleanData.gen_data_report` on its own, forces an overwrite of the outputs (`CleanData.report_df` and output file), and has some bugs w.r.t the data dictionary. This ought to be fixed in a future update.

#### Relevant Definitions Settings
* **INITIAL_REPORT_FILENAME**: output file name to store the initial report prior to optional cleaning steps. E.g. "`initialisation_report.xlsx`"

### Examples

```
print(cd.report_df)
```

#### Sample Output
```
                data_type data_type_in_dict data_type_mismatch  count_missing_values  percentage_missing_values numeric_range                     unique_categories
TESTID              int64           numeric            Matched                     0                     0.0000       1:10000                                  N.A.
ID                  int64           numeric            Matched                     0                     0.0000   51624:71915                                  N.A.
SurveyYr           object            string            Matched                     0                     0.0000           NaN                       2009_10,2011_12
Gender             object            string            Matched                     0                     0.0000           NaN                           male,female
Age                 int64           numeric            Matched                     0                     0.0000          0:80                                  N.A.
...                   ...               ...                ...                   ...                        ...           ...                                   ...
SexNumPartnLife   float64           numeric            Matched                  4275                     0.4275    0.0:2000.0                                  N.A.
SexNumPartYear    float64           numeric            Matched                  5072                     0.5072      0.0:69.0                                  N.A.
SameSex            object            string            Matched                  4232                     0.4232           NaN                            No,nan,Yes
SexOrientation     object            string            Matched                  5158                     0.5158           NaN  Heterosexual,nan,Bisexual,Homosexual
PregnantNow        object            string            Matched                  8304                     0.8304           NaN                    nan,No,Unknown,Yes
```

The function can also be used to generate reports after the cleaning is done. 

```
cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df)
print(cd.report_df)
```

#### Sample Output
```
Initial Report Generated: filename: */examples/trainData/initialisation_report.xlsx
                data_type data_type_in_dict data_type_mismatch  count_missing_values  percentage_missing_values numeric_range                          unique_categories
TESTID              int64           numeric            Matched                     0                   0.000000       1:10000                                       N.A.
ID                  int64           numeric            Matched                     0                   0.000000   51624:71915                                       N.A.
SurveyYr           object            string            Matched                     0                   0.000000           NaN                            2009_10,2011_12
Gender             string            string  Possible mismatch                     0                   0.000000           NaN                                male,female
Age                 Int64           numeric  Possible mismatch                     0                   0.000000          0:80                                       N.A.
...                   ...               ...                ...                   ...                        ...           ...                                        ...
SexNumPartnLife     Int64           numeric  Possible mismatch                  3727                   0.475868        0:2000                                       N.A.
SexNumPartYear      Int64           numeric  Possible mismatch                  4333                   0.553243          0:69                                       N.A.
SameSex            string            string  Possible mismatch                  3695                   0.471782           NaN                            No,<NA>,Yes,UNK
SexOrientation     string            string  Possible mismatch                     0                   0.000000           NaN  Heterosexual,N.A.,Bisexual,UNK,Homosexual
PregnantNow        string            string  Possible mismatch                     0                   0.000000           NaN                    UNK,N.A.,No,Unknown,Yes
```