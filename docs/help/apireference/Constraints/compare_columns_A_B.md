---
layout: default
title: Compare Columns A and B
parent: Constraints
grand_parent: API Reference
nav_order: 2
---

# Constraints.compare_columns_A_B

A function to compare two columns A and B of a dataframe and modify column A to B's value if A is greater than B

**Constraints.compare_columns_A_B(*df*, *A*, *B*)**

**Parameters**
- *df*: (dataframe)
  - dataframe that contains the two columns
- *A*: (str)
  - name of the first column
- *B*: (str)
  - name of the second column

**Returns**
- pandas.DataFrame
  - modified dataframe with column A equal to B if A was greater

### Notes

### Examples

#### FIX nPregnancies, nBabies, Age1stBaby (numerical)
```
# nPregnancies: How many times participant has been pregnant. Reported for female participants aged 20 years or older
# nBabies: How many of participants deliveries resulted in live births. Reported for female participants aged 20 years or older.
# Age1stBaby: Age of participant at time of first live birth. 14 years or under = 14, 45 years or older = 45. Reported for female participants aged 20 years or older.
# nBabies <= nPregnancies, else nBabies=nPregnancies
# Age1stBaby <= Age, else Age1stBaby=Age

df = con.compare_columns_A_B(df, 'nBabies', 'nPregnancies')
df = con.compare_columns_A_B(df, 'Age1stBaby', 'Age')
```