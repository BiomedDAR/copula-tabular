---
layout: default
title: Convert Blanks to Value
parent: Constraints
grand_parent: API Reference
nav_order: 3
---

# Constraints.convertBlankstoValue

This function is used to convert missing values in a dataframe column to a specified value.

**Constraints.convertBlankstoValue(*df*, [*var_array*, *value*])**

**Parameters**
- *df*: (dataframe)
  - dataframe that contains the two columns
- *var_array*: (list)
  - an array of variable names that need to be processed.
  - default is `None`. No variables will be modified
- *value*: (str)
  - the replacement value to be given for missing values.
  - if `None`, `"UNK"` is used as default

**Returns**
- pandas.DataFrame
  - modified dataframe

### Notes
*   Raises ValueError: if the variable is not found in the given dataframe.

### Examples

```
 # Load the dataframe
df = pd.read_csv('data.csv')

# Create an array of variables
var_array = ['Var1', 'Var2', 'Var3']

# Convert missing values in the dataframe to 'UNK'
convertBlankstoValue(df, var_array, value='UNK')
```