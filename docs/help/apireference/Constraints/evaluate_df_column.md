---
layout: default
title: Evaluate DF Column
parent: Constraints
grand_parent: API Reference
nav_order: 4
---

# Constraints.evaluate_df_column

This function takes a dataframe and column name(s) and evaluates the column based on the given conditions and values, creating a new column in the dataframe with the evaluated values. Optionally, a function can be passed in to evaluate the column.

**Constraints.evaluate_df_column(*df*, *column_names*, [*dict_conditions_values*, *func*, *output_column_name*])**

**Parameters**
- *df*: (dataframe)
  - dataframe to be evaluated
- *column_names*: (str, list)
  - a string or list of strings containing the name(s) of the columns to be evaluated
- *dict_conditions_values*: (dict)
  - A dictionary containing the conditions and values to be evaluated. E.g. dict_conditions_values = {i: {condition: lambda x: x> 5 OR "x>5", value: "'5+'"} }
- *func*: (function)
  - A function to be applied on the columns
  - Default is `None`
- *output_column_name*: (str)
  - A string containing the name of the output column. If not provided, the default is the name of the column plus '_evaluated'.

**Returns**
- pandas.DataFrame
  - the dataframe with the evaluated values in the new column

### Notes

Snippet of an example `dict_conditions_values`
```
df = evaluate_df_column(df, 'item', dict_conditions_values=
    {
        'condition_1': {'condition': 'x == "apples"', 'value': '"fruit"'},
        'condition_2': {'condition': 'x == "oranges"', 'value': '"fruit"'},
        'condition_3': {'condition': 'x == "carrots"', 'value': '"vegetable"'},
        'condition_4': {'condition': 'x == "potatoes"', 'value': '"vegetable"'}
    },
    output_column_name='item_type'
)
```

### Examples

#### Creating AgeDecade as a secondary variable from Age
```
dict_conditions_values = {}
for i in range(1,11):
    if (i-1)*10 >= 70:
        value = ' 70+'
    else:
        value = f" {(i-1)*10}-{i*10-1}"  #' 0-9'
    dict_conditions_values.update({str(i): {
        'condition': f"{(i-1)*10} <= x and x < {i*10}", #"0 < x and x < 10",
        'value': f"'{value}'"
    }})
df = con.evaluate_df_column(df, 'Age', dict_conditions_values, output_column_name="AgeDecade")
```

#### Generating Smoke100n from Smoke100 (convert 'Yes' to 'Smoker', 'No' to 'Non-Smoker') using customised function
```
<!-- Build customised function -->
def compute_smoke100n(df_row):
    w = df_row['Smoke100']
    smoke100n = "N.A."
    if (w=='Yes'):
        smoke100n = 'Smoker'
    elif (w=='No'):
        smoke100n = 'Non-Smoker'
    else:
        smoke100n = w

    return smoke100n

df = con.evaluate_df_column(df, ['Smoke100'], func=compute_smoke100n, output_column_name='Smoke100n')
```

#### Derive secondary variable HHIncomeMid from HHIncome
```
def fn_1(x):
    if "-" in str(x):
        v = x.split("-")
        return ( int(v[1]) + 1 + int(v[0]) )/ 2
    elif "UNK" in str(x):
        return np.nan
    elif "more" in str(x):
        return 100000
    else:
        return np.nan
        
con.evaluate_df_column(df, 'HHIncome', func=fn_1, output_column_name='HHIncomeMid')
```
