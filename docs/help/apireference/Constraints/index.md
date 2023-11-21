---
layout: default
title: Constraints
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# Constraints

`class Constraits(debug=False, logging=True, logger=None)`
Module for building customised constraints for data cleaning. Designed to work with the [CleanData](../CleanData/) class.

### Parameters

**debug**: boolean, default `False`. Whether to print debug-related outputs to console.

**logging**: boolean, default `True`. Whether to generate logfile.

**logger**: object, default is `None`. If `None`, and `logging==True`, logs will be printed to the `constraints_logfile.txt` file. Alternatively, one can supply the `CleanData.logger` object for continuous logging.

### Notes
The `Constraints` class contains methods which are commonly used as building blocks for more complicated constraints.  The methods support automatic logging. One way to use these methods to modify a variable is to write a wrapper function for variable `variableOne`, and call it in a script.py:

```
def con_variableOne(df, con=con)
    # use a method in con
    df = con.method(df,[ ...] )

    return df, con

df = cd.clean_df
con = Constraints(debug=True, logging=True, logger=cd.logger)
df, con = con_variable(df, con)

<!-- Check details of constrained dataset -->
pprint.pprint(con.log)

<!-- Output log variable to file -->
con.output_log_to_file()

<!-- Update CleanData with new DF -->
cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)
```

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [CleanData 3](../../../gettingStarted/examples/CleanDataWithConstraints) | Demonstrates use of customised constraints |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug | (boolean) whether to debug or not  |
| logging | (boolean) whether to log or not |
| logger | (obj) logger used for logging |
| log | (dict) dictionary that records things done to a variable |

### Methods

| Method         | Description | 
| ---:              |    :----   |
| output_log_to_file() | Output the collected information in Constraints.log to log file. |
| multiparent_conditions(df, var_array, dict_conditions_values) | Function for replacement of values in a dataframe based on multiple conditions evaluated from multiple columns.|
| evaluate_df_column(df, column_names, [dict_conditions_values, func, output_column_name]) | This function takes a dataframe and column name(s) and evaluates the column based on the given conditions and values, creating a new column in the dataframe with the evaluated values. Optionally, a function can be passed in to evaluate the column.|
| convertBlankstoValue(df, [var_array, value]) | This function is used to convert missing values in a dataframe column to a specified value.|
| compare_columns_A_B(df, A, B) | A function to compare two columns A and B of a dataframe and modify column A to B's value if A is greater than B |