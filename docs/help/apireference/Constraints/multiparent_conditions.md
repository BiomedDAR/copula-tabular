---
layout: default
title: Multiparent Conditions
parent: Constraints
grand_parent: API Reference
nav_order: 5
---

# Constraints.multiparent_conditions

Function for replacement of values in a dataframe based on multiple conditions evaluated from multiple columns.

**Constraints.multiparent_conditions(*df*, *var_array*, *dict_conditions_values*)**

**Parameters**
- *df*: (dataframe)
  - dataframe to be updated
- *var_array*: (list)
  - A list of strings of column names to be updated.
- *dict_conditions_values*: (dict)
  - A dictionary of conditions and values. The conditions are evaluated from multiple columns and the corresponding value is then inserted into the specified columns.

**Returns**
- pandas.DataFrame
  - the updated dataframe

### Notes

Snippet of an example `dict_conditions_values`
```
df = multiparent_conditions(df, ["column1", "column2"], 
    {0: 
        {
            "conditions": {
                "parent1": {"parent": "parent1_column", "condition": "> 5"}, 
                "parent2": {"parent": "parent2_column", "condition": "< 10"}
            }, 
            "value": 0
        }, 
    1: {
            "conditions": {
                "parent3": {"parent": "parent3_column", "condition": "== 'Yes'"}
            }, 
            "value": 1 #note that assigned value must match the dtype of column
        }
    }
)
```
This example updates the dataframe with the values `0` and `1` in `"column1"` and `"column2"` columns, according to the conditions given. In particular, the value `0` is inserted when `"parent1_column"` is greater than `5` AND `"parent2_column"` is less than `10`. The value `1` is inserted when `"parent3_column"` is equal to `"Yes"`.

### Examples

#### FIX nPregnancies, nBabies, Age1stBaby (numerical)
```
# nPregnancies: How many times participant has been pregnant. Reported for female participants aged 20 years or older
# nBabies: How many of participants deliveries resulted in live births. Reported for female participants aged 20 years or older.
# Age1stBaby: Age of participant at time of first live birth. 14 years or under = 14, 45 years or older = 45. Reported for female participants aged 20 years or older.

vArray = ['nPregnancies', 'nBabies', 'Age1stBaby']
age_lessthan20 = {'parent': 'Age', 'condition': '<20'}
genderisMale = {'parent': 'Gender', 'condition': '=="male"'}
dict_conditions_values = {
    1: {
        'conditions': {1: age_lessthan20},
        'value': np.nan
    },
    2: {
        'conditions': {1: genderisMale},
        'value': np.nan
    }
}
df = con.multiparent_conditions(df, vArray, dict_conditions_values)
```