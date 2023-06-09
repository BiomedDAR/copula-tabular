---
layout: default
title: Example for Constraints
parent: Examples
grand_parent: Getting Started
nav_order: 4
---

### Example 1 (Constrain a value using multiple parent conditions)
In this example, we demonstrate the use of the `multiparent_conditions` function of the Constraints class. We are constraining the variable `AgeMonths` with the following:
*   If SurveyYr=='2009_10' and Age>=80, AgeMonths = ''
*   If SurveyYr=='2009_10' and AgeMonths>=948, AgeMonths = ''
*   If SurveyYr=='2011_12' and Age>=3, AgeMonths = ''
*   If SurveyYr=='2011_12' and AgeMonths>=24, AgeMonths = ''

To do so, we use the `multiparent_conditions` function, which is able to update a set of variables based on a dictionary of conditions/values.

To stipulate the condition `If SurveyYr=='2009_10' and Age>=80, AgeMonths = ''`, we define two dictionaries, one for each parent variable (`SurveyYr` and `Age`), namely as:
```
surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
age_morethan80 = {'parent': 'Age', 'condition': '>=80'}
```
and append them to a dictionary `dict_conditions_values`, under `conditions`. Under the `value` field, we stipulate the value to assign the row should the conditions be fulfilled.
```
dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10, 2: age_morethan80},
            'value': np.nan
        }
}
```
We continue the above for each condition, and obtain the full function as below:

```
# Fix AgeMonths variable
def con_ageMonths(df, con=con):

    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    surveyYr_2011_12 = {'parent': 'SurveyYr', 'condition': '=="2011_12"'}
    age_morethan80 = {'parent': 'Age', 'condition': '>=80'}
    age_morethan3 = {'parent': 'Age', 'condition': '>=3'}
    ageMonths_morethan948 = {'parent': 'AgeMonths', 'condition': '>=948'}
    ageMonths_morethan24 = {'parent': 'AgeMonths', 'condition': '>=24'}
    dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10, 2: age_morethan80},
            'value': np.nan
        },
        2: {
            'conditions': {1: surveyYr_2009_10, 2: ageMonths_morethan948},
            'value': np.nan
        },
        3: {
            'conditions': {1: surveyYr_2011_12, 2: age_morethan3},
            'value': np.nan
        },
        4: {
            'conditions': {1: surveyYr_2011_12, 2: ageMonths_morethan24},
            'value': np.nan
        }
    }

    var_array = ['AgeMonths']
    df = con.multiparent_conditions(df, var_array, dict_conditions_values)

    return df, con
```
Please refer to the previous [example](CleanDataWithConstraints) for details on how to use this function with the CleanData class.

### Example 2 (Convert missing values in a dataframe column to specified value)
In this example, we demonstrate the use of the `convertBlankstoValue` function of the Constraints class. We are constraining the variable `Race3` with the following:
*   If SurveyYr=='2009_10', Race3 = 'N.A.'
At the same time, we need to convert all empty (missing values) cells into `UNK`, so as to differentiate it from `N.A.`.

To do so, we use the `convertBlankstoValue` function, which is able to convert missing values in a dataframe column to a specified value, together with the `multiparent_conditions` function.

```
# Convert categorical blanks to UNK
vArray = ['Race1', 'Race3'] # set the variables to convert
df = con.convertBlankstoValue(df, var_array=vArray, value='UNK')
```

We incorporate the above in a function as seen below:

```
# FIX Race3 variable (categorical)
def con_Race3(df, con=con):

    # Convert categorical blanks to UNK
    vArray = ['Race1', 'Race3']
    df = con.convertBlankstoValue(df, var_array=vArray, value='UNK')

    # If SurveyYr=='2009_10', Race3 = '(blanks)'
    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10},
            'value': 'N.A.'
        }
    }
    df = con.multiparent_conditions(df, ['Race3'], dict_conditions_values)

    return df, con
```

Please refer to the previous [example](CleanDataWithConstraints) for details on how to use this function with the CleanData class.


### Example 3 (Generate new variables)
In this example, we demonstrate the use of the `evaluate_df_column` function of the Constraints class, to generate new variables for use. We will be creating the variable `BMI` using the data (`Height` and `Weight`) reported for participants aged 2 years or older.

We first write a function `compute_bmi` which computes the BMI for every subject (dataframe row).
```
def compute_bmi(df_row):
    w = df_row['Weight']
    h = df_row['Height']
    if any(pd.isnull(value) for value in df_row):
        BMI = np.nan
    else:
        h2 = h / 100
        BMI = w / (h2 * h2)
        BMI = round(BMI, 2)

    return BMI
```

Next, we can use this function as an input to `evaluate_df_column` to generate a new column (`BMI`) in the dataframe.
```
df = con.evaluate_df_column(df, ['Height', 'Weight'], func=compute_bmi, output_column_name="BMI")
```

### Example 4 (Modify A to B if A>B)
In this example, we demonstrate the use of the `compare_columns_A_B` function of the Constraints class. This function compares two columns A and B of a dataframe and modifies column A to B's value if A is greater than B. We will be constraining the variable `nBabies` to be less than or equal to `nPregnancies`.

```
df = con.compare_columns_A_B(df, 'nBabies', 'nPregnancies')
```
