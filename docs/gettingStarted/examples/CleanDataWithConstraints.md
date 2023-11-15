---
layout: default
title: Example for CleanData class with Constraints
parent: Examples
grand_parent: Getting Started
nav_order: 3
---

## Example of CleanData with Constraints Class
This example demonstrates the use of the CleanData class together with the Constraints class. It continues from the previous [example](CleanData).

### Print Report
Before we exert the constraints, we can take a look at the data report, which is automatically generated during initialisation.
```
cd = CleanData(definitions=defi)
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

### Import Libraries
```
# LOAD DEPENDENCIES
from mz.Constraints import Constraints
```

eg_nhanes_constraints is a script where the constraints specific to the nhanes have been stored. They consists of functions which take in a dataframe from the CleanData class and an object of the Constraints class, and returns a constrained dataframe and an updated Constraints class that captured the details of the transformation.
```
import eg_nhanes_constraints as n_con
```

### Use Constraints
Load the dataframe from the CleanData object. Initialise a new Constraints object.
```
df = cd.clean_df
con = Constraints(debug=True)
```

The following are examples of constraints used on the variables of the NHANES dataset. The dataset undergoes a series of constraints, as stipulated by the metadata. Please refer to the [Constraints example](Constraints) for further details on their usage/construction.
```
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
```

#### Sample output
```
For variable: AgeDecade: Replaced AgeDecade using conditions and values given in dict_conditions_values.
For variable: AgeDecade: Converted 0 missing values to UNK.
For variable: AgeMonths: Replaced AgeMonths using conditions and values given in dict_conditions_values.
For variable: Race1: Converted 0 missing values to UNK.
For variable: Race3: Converted 3568 missing values to UNK.
For variable: Race3: Replaced Race3 using conditions and values given in dict_conditions_values.
For variable: Gender: Converted 0 missing values to UNK.
For variable: Education: Converted 2363 missing values to UNK.
For variable: MaritalStatus: Converted 2358 missing values to UNK.
For variable: Education: Replaced Education using conditions and values given in dict_conditions_values.
For variable: MaritalStatus: Replaced MaritalStatus using conditions and values given in dict_conditions_values.
For variable: HHIncome: Converted 653 missing values to UNK.
For variable: HHIncomeMid: Replaced HHIncomeMid using conditions and values given in dict_conditions_values.
For variable: Poverty: Replaced Poverty using conditions and values given in dict_conditions_values.
For variable: Poverty: Converted 665 missing values to nan.
For variable: HomeOwn: Converted 50 missing values to UNK.
For variable: Work: Converted 1922 missing values to UNK.
For variable: Length: Replaced Length using conditions and values given in dict_conditions_values.
For variable: HeadCirc: Replaced HeadCirc using conditions and values given in dict_conditions_values.
For variable: Height: Replaced Height using conditions and values given in dict_conditions_values.
For variable: BMI: Replaced BMI using conditions and values given in dict_conditions_values.
For variable: BMICatUnder20yrs: Replaced BMICatUnder20yrs using conditions and values given in dict_conditions_values.
For variable: BMI_WHO: Replaced BMI_WHO using conditions and values given in dict_conditions_values.
For variable: Testosterone: Replaced Testosterone using conditions and values given in dict_conditions_values.
For variable: DirectChol: Replaced DirectChol using conditions and values given in dict_conditions_values.
For variable: TotChol: Replaced TotChol using conditions and values given in dict_conditions_values.
For variable: UrineVol1: Replaced UrineVol1 using conditions and values given in dict_conditions_values.
For variable: UrineFlow1: Replaced UrineFlow1 using conditions and values given in dict_conditions_values.
For variable: UrineVol2: Replaced UrineVol2 using conditions and values given in dict_conditions_values.
For variable: UrineFlow2: Replaced UrineFlow2 using conditions and values given in dict_conditions_values.
For variable: Diabetes: Converted 133 missing values to UNK.
For variable: Diabetes: Replaced Diabetes using conditions and values given in dict_conditions_values.
For variable: DiabetesAge: Replaced DiabetesAge using conditions and values given in dict_conditions_values.
For variable: DiabetesAge: Converted 0 values in DiabetesAge to Age.
For variable: HealthGen: Converted 2067 missing values to UNK.
For variable: HealthGen: Replaced HealthGen using conditions and values given in dict_conditions_values.
For variable: DaysPhysHlthBad: Replaced DaysPhysHlthBad using conditions and values given in dict_conditions_values.
For variable: DaysMentHlthBad: Replaced DaysMentHlthBad using conditions and values given in dict_conditions_values.
For variable: LittleInterest: Converted 2783 missing values to UNK.
For variable: Depressed: Converted 2781 missing values to UNK.
For variable: LittleInterest: Replaced LittleInterest using conditions and values given in dict_conditions_values.
For variable: Depressed: Replaced Depressed using conditions and values given in dict_conditions_values.
For variable: nPregnancies: Replaced nPregnancies using conditions and values given in dict_conditions_values.
For variable: nBabies: Replaced nBabies using conditions and values given in dict_conditions_values.
For variable: Age1stBaby: Replaced Age1stBaby using conditions and values given in dict_conditions_values.
For variable: nBabies: Converted 0 values in nBabies to nPregnancies.
For variable: Age1stBaby: Converted 1 values in Age1stBaby to Age.
For variable: SleepHrsNight: Replaced SleepHrsNight using conditions and values given in dict_conditions_values.
For variable: SleepTrouble: Converted 1921 missing values to UNK.
For variable: SleepTrouble: Replaced SleepTrouble using conditions and values given in dict_conditions_values.
For variable: PhysActive: Converted 1458 missing values to UNK.
For variable: PhysActive: Replaced PhysActive using conditions and values given in dict_conditions_values.
For variable: PhysActiveDays: Replaced PhysActiveDays using conditions and values given in dict_conditions_values.
For variable: TVHrsDay: Converted 3704 missing values to UNK.
For variable: CompHrsDay: Converted 3700 missing values to UNK.
For variable: TVHrsDay: Replaced TVHrsDay using conditions and values given in dict_conditions_values.
For variable: CompHrsDay: Replaced CompHrsDay using conditions and values given in dict_conditions_values.
For variable: TVHrsDayChild: Replaced TVHrsDayChild using conditions and values given in dict_conditions_values.
For variable: CompHrsDayChild: Replaced CompHrsDayChild using conditions and values given in dict_conditions_values.
For variable: Alcohol12PlusYr: Converted 2853 missing values to UNK.
For variable: Alcohol12PlusYr: Replaced Alcohol12PlusYr using conditions and values given in dict_conditions_values.
For variable: AlcoholDay: Replaced AlcoholDay using conditions and values given in dict_conditions_values.
For variable: AlcoholYear: Replaced AlcoholYear using conditions and values given in dict_conditions_values.
For variable: Smoke100: Converted 2354 missing values to UNK.
For variable: Smoke100: Replaced Smoke100 using conditions and values given in dict_conditions_values.
For variable: SmokeNow: Converted 5409 missing values to UNK.
For variable: SmokeNow: Replaced SmokeNow using conditions and values given in dict_conditions_values.
For variable: Smoke100n: Replaced Smoke100n using conditions and values given in dict_conditions_values.
For variable: SmokeAge: Replaced SmokeAge using conditions and values given in dict_conditions_values.
For variable: SmokeAge: Converted 0 values in SmokeAge to Age.
For variable: Marijuana: Converted 4163 missing values to UNK.
For variable: RegularMarij: Converted 4163 missing values to UNK.
For variable: Marijuana: Replaced Marijuana using conditions and values given in dict_conditions_values.
For variable: RegularMarij: Replaced RegularMarij using conditions and values given in dict_conditions_values.
For variable: AgeFirstMarij: Replaced AgeFirstMarij using conditions and values given in dict_conditions_values.
For variable: AgeRegMarij: Replaced AgeRegMarij using conditions and values given in dict_conditions_values.
For variable: AgeFirstMarij: Replaced AgeFirstMarij using conditions and values given in dict_conditions_values.
For variable: AgeRegMarij: Replaced AgeRegMarij using conditions and values given in dict_conditions_values.
For variable: AgeFirstMarij: Converted 0 values in AgeFirstMarij to Age.
For variable: AgeRegMarij: Converted 0 values in AgeRegMarij to Age.
For variable: HardDrugs: Converted 3521 missing values to UNK.
For variable: SexEver: Converted 3520 missing values to UNK.
For variable: SameSex: Converted 3520 missing values to UNK.
For variable: HardDrugs: Replaced HardDrugs using conditions and values given in dict_conditions_values.
For variable: SexEver: Replaced SexEver using conditions and values given in dict_conditions_values.
For variable: SameSex: Replaced SameSex using conditions and values given in dict_conditions_values.
For variable: SameSex: Replaced SameSex using conditions and values given in dict_conditions_values.
For variable: SexAge: Replaced SexAge using conditions and values given in dict_conditions_values.
For variable: SexNumPartnLife: Replaced SexNumPartnLife using conditions and values given in dict_conditions_values.
For variable: SexAge: Converted 0 values in SexAge to Age.
For variable: SexNumPartYear: Replaced SexNumPartYear using conditions and values given in dict_conditions_values.
For variable: SexOrientation: Converted 4245 missing values to UNK.
For variable: SexOrientation: Replaced SexOrientation using conditions and values given in dict_conditions_values.
For variable: PregnantNow: Converted 6540 missing values to UNK.
For variable: PregnantNow: Replaced PregnantNow using conditions and values given in dict_conditions_values.
```

### Check Output
Check details of the constrained dataset
```
pprint.pprint(con.log)
```

#### Sample Output
```
{'Age1stBaby': {'compare_columns_A_B': 'Converted 1 values in Age1stBaby to '
                                       'Age.',
                'evaluate_df_column': 'Replaced Age1stBaby using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'AgeDecade': {'convertBlankstoValue': 'Converted 0 missing values to UNK.',
               'evaluate_df_column': 'Replaced AgeDecade using conditions and '
                                     'values given in dict_conditions_values.'},
 'AgeFirstMarij': {'compare_columns_A_B': 'Converted 0 values in AgeFirstMarij '
                                          'to Age.',
                   'evaluate_df_column': 'Replaced AgeFirstMarij using '
                                         'conditions and values given in '
                                         'dict_conditions_values.'},
 'AgeMonths': {'evaluate_df_column': 'Replaced AgeMonths using conditions and '
                                     'values given in dict_conditions_values.'},
 'AgeRegMarij': {'compare_columns_A_B': 'Converted 0 values in AgeRegMarij to '
                                        'Age.',
                 'evaluate_df_column': 'Replaced AgeRegMarij using conditions '
                                       'and values given in '
                                       'dict_conditions_values.'},
 'Alcohol12PlusYr': {'convertBlankstoValue': 'Converted 2853 missing values to '
                                             'UNK.',
                     'evaluate_df_column': 'Replaced Alcohol12PlusYr using '
                                           'conditions and values given in '
                                           'dict_conditions_values.'},
 'AlcoholDay': {'evaluate_df_column': 'Replaced AlcoholDay using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'AlcoholYear': {'evaluate_df_column': 'Replaced AlcoholYear using conditions '
                                       'and values given in '
                                       'dict_conditions_values.'},
 'BMI': {'evaluate_df_column': 'Replaced BMI using conditions and values given '
                               'in dict_conditions_values.'},
 'BMICatUnder20yrs': {'evaluate_df_column': 'Replaced BMICatUnder20yrs using '
                                            'conditions and values given in '
                                            'dict_conditions_values.'},
 'BMI_WHO': {'evaluate_df_column': 'Replaced BMI_WHO using conditions and '
                                   'values given in dict_conditions_values.'},
 'CompHrsDay': {'convertBlankstoValue': 'Converted 3700 missing values to UNK.',
                'evaluate_df_column': 'Replaced CompHrsDay using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'CompHrsDayChild': {'evaluate_df_column': 'Replaced CompHrsDayChild using '
                                           'conditions and values given in '
                                           'dict_conditions_values.'},
 'DaysMentHlthBad': {'evaluate_df_column': 'Replaced DaysMentHlthBad using '
                                           'conditions and values given in '
                                           'dict_conditions_values.'},
 'DaysPhysHlthBad': {'evaluate_df_column': 'Replaced DaysPhysHlthBad using '
                                           'conditions and values given in '
                                           'dict_conditions_values.'},
 'Depressed': {'convertBlankstoValue': 'Converted 2781 missing values to UNK.',
               'evaluate_df_column': 'Replaced Depressed using conditions and '
                                     'values given in dict_conditions_values.'},
 'Diabetes': {'convertBlankstoValue': 'Converted 133 missing values to UNK.',
              'evaluate_df_column': 'Replaced Diabetes using conditions and '
                                    'values given in dict_conditions_values.'},
 'DiabetesAge': {'compare_columns_A_B': 'Converted 0 values in DiabetesAge to '
                                        'Age.',
                 'evaluate_df_column': 'Replaced DiabetesAge using conditions '
                                       'and values given in '
                                       'dict_conditions_values.'},
 'DirectChol': {'evaluate_df_column': 'Replaced DirectChol using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'Education': {'convertBlankstoValue': 'Converted 2363 missing values to UNK.',
               'evaluate_df_column': 'Replaced Education using conditions and '
                                     'values given in dict_conditions_values.'},
 'Gender': {'convertBlankstoValue': 'Converted 0 missing values to UNK.'},
 'HHIncome': {'convertBlankstoValue': 'Converted 653 missing values to UNK.'},
 'HHIncomeMid': {'evaluate_df_column': 'Replaced HHIncomeMid using conditions '
                                       'and values given in '
                                       'dict_conditions_values.'},
 'HardDrugs': {'convertBlankstoValue': 'Converted 3521 missing values to UNK.',
               'evaluate_df_column': 'Replaced HardDrugs using conditions and '
                                     'values given in dict_conditions_values.'},
 'HeadCirc': {'evaluate_df_column': 'Replaced HeadCirc using conditions and '
                                    'values given in dict_conditions_values.'},
 'HealthGen': {'convertBlankstoValue': 'Converted 2067 missing values to UNK.',
               'evaluate_df_column': 'Replaced HealthGen using conditions and '
                                     'values given in dict_conditions_values.'},
 'Height': {'evaluate_df_column': 'Replaced Height using conditions and values '
                                  'given in dict_conditions_values.'},
 'HomeOwn': {'convertBlankstoValue': 'Converted 50 missing values to UNK.'},
 'Length': {'evaluate_df_column': 'Replaced Length using conditions and values '
                                  'given in dict_conditions_values.'},
 'LittleInterest': {'convertBlankstoValue': 'Converted 2783 missing values to '
                                            'UNK.',
                    'evaluate_df_column': 'Replaced LittleInterest using '
                                          'conditions and values given in '
                                          'dict_conditions_values.'},
 'Marijuana': {'convertBlankstoValue': 'Converted 4163 missing values to UNK.',
               'evaluate_df_column': 'Replaced Marijuana using conditions and '
                                     'values given in dict_conditions_values.'},
 'MaritalStatus': {'convertBlankstoValue': 'Converted 2358 missing values to '
                                           'UNK.',
                   'evaluate_df_column': 'Replaced MaritalStatus using '
                                         'conditions and values given in '
                                         'dict_conditions_values.'},
 'PhysActive': {'convertBlankstoValue': 'Converted 1458 missing values to UNK.',
                'evaluate_df_column': 'Replaced PhysActive using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'PhysActiveDays': {'evaluate_df_column': 'Replaced PhysActiveDays using '
                                          'conditions and values given in '
                                          'dict_conditions_values.'},
 'Poverty': {'convertBlankstoValue': 'Converted 665 missing values to nan.',
             'evaluate_df_column': 'Replaced Poverty using conditions and '
                                   'values given in dict_conditions_values.'},
 'PregnantNow': {'convertBlankstoValue': 'Converted 6540 missing values to '
                                         'UNK.',
                 'evaluate_df_column': 'Replaced PregnantNow using conditions '
                                       'and values given in '
                                       'dict_conditions_values.'},
 'Race1': {'convertBlankstoValue': 'Converted 0 missing values to UNK.'},
 'Race3': {'convertBlankstoValue': 'Converted 3568 missing values to UNK.',
           'evaluate_df_column': 'Replaced Race3 using conditions and values '
                                 'given in dict_conditions_values.'},
 'RegularMarij': {'convertBlankstoValue': 'Converted 4163 missing values to '
                                          'UNK.',
                  'evaluate_df_column': 'Replaced RegularMarij using '
                                        'conditions and values given in '
                                        'dict_conditions_values.'},
 'SameSex': {'convertBlankstoValue': 'Converted 3520 missing values to UNK.',
             'evaluate_df_column': 'Replaced SameSex using conditions and '
                                   'values given in dict_conditions_values.'},
 'SexAge': {'compare_columns_A_B': 'Converted 0 values in SexAge to Age.',
            'evaluate_df_column': 'Replaced SexAge using conditions and values '
                                  'given in dict_conditions_values.'},
 'SexEver': {'convertBlankstoValue': 'Converted 3520 missing values to UNK.',
             'evaluate_df_column': 'Replaced SexEver using conditions and '
                                   'values given in dict_conditions_values.'},
 'SexNumPartYear': {'evaluate_df_column': 'Replaced SexNumPartYear using '
                                          'conditions and values given in '
                                          'dict_conditions_values.'},
 'SexNumPartnLife': {'evaluate_df_column': 'Replaced SexNumPartnLife using '
                                           'conditions and values given in '
                                           'dict_conditions_values.'},
 'SexOrientation': {'convertBlankstoValue': 'Converted 4245 missing values to '
                                            'UNK.',
                    'evaluate_df_column': 'Replaced SexOrientation using '
                                          'conditions and values given in '
                                          'dict_conditions_values.'},
 'SleepHrsNight': {'evaluate_df_column': 'Replaced SleepHrsNight using '
                                         'conditions and values given in '
                                         'dict_conditions_values.'},
 'SleepTrouble': {'convertBlankstoValue': 'Converted 1921 missing values to '
                                          'UNK.',
                  'evaluate_df_column': 'Replaced SleepTrouble using '
                                        'conditions and values given in '
                                        'dict_conditions_values.'},
 'Smoke100': {'convertBlankstoValue': 'Converted 2354 missing values to UNK.',
              'evaluate_df_column': 'Replaced Smoke100 using conditions and '
                                    'values given in dict_conditions_values.'},
 'Smoke100n': {'evaluate_df_column': 'Replaced Smoke100n using conditions and '
                                     'values given in dict_conditions_values.'},
 'SmokeAge': {'compare_columns_A_B': 'Converted 0 values in SmokeAge to Age.',
              'evaluate_df_column': 'Replaced SmokeAge using conditions and '
                                    'values given in dict_conditions_values.'},
 'SmokeNow': {'convertBlankstoValue': 'Converted 5409 missing values to UNK.',
              'evaluate_df_column': 'Replaced SmokeNow using conditions and '
                                    'values given in dict_conditions_values.'},
 'TVHrsDay': {'convertBlankstoValue': 'Converted 3704 missing values to UNK.',
              'evaluate_df_column': 'Replaced TVHrsDay using conditions and '
                                    'values given in dict_conditions_values.'},
 'TVHrsDayChild': {'evaluate_df_column': 'Replaced TVHrsDayChild using '
                                         'conditions and values given in '
                                         'dict_conditions_values.'},
 'Testosterone': {'evaluate_df_column': 'Replaced Testosterone using '
                                        'conditions and values given in '
                                        'dict_conditions_values.'},
 'TotChol': {'evaluate_df_column': 'Replaced TotChol using conditions and '
                                   'values given in dict_conditions_values.'},
 'UrineFlow1': {'evaluate_df_column': 'Replaced UrineFlow1 using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'UrineFlow2': {'evaluate_df_column': 'Replaced UrineFlow2 using conditions '
                                      'and values given in '
                                      'dict_conditions_values.'},
 'UrineVol1': {'evaluate_df_column': 'Replaced UrineVol1 using conditions and '
                                     'values given in dict_conditions_values.'},
 'UrineVol2': {'evaluate_df_column': 'Replaced UrineVol2 using conditions and '
                                     'values given in dict_conditions_values.'},
 'Work': {'convertBlankstoValue': 'Converted 1922 missing values to UNK.'},
 'nBabies': {'compare_columns_A_B': 'Converted 0 values in nBabies to '
                                    'nPregnancies.',
             'evaluate_df_column': 'Replaced nBabies using conditions and '
                                   'values given in dict_conditions_values.'},
 'nPregnancies': {'evaluate_df_column': 'Replaced nPregnancies using '
                                        'conditions and values given in '
                                        'dict_conditions_values.'}}
```

### Update CleanData class
Update the CleanData class with constrained data. 
```
cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)
```

#### Sample Output
```
Replacing the input data...
Replacing the input data complete. new filename: *\trainData\nhanes_raw-DD-CON.csv
```