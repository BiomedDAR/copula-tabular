---
layout: default
title: Transformer
parent: API Reference
grand_parent: Help and Reference
nav_order: 1
has_children: true
---

# Transformer

`class Transformer(metaData=None, definitions=None, default_transformer_type_4_string='One-Hot', default_datetime_format=f'%Y-%m-%d %H:%M:%S', var_list=None, removeNull=False, debug=False)`
Module for transformation of data into numerical equivalents for further processing.

### Parameters

**metaData**: dict, optional, default `None`. To specify transformation instructions for specific variables.

**definitions**:  file (.py), optional, default `None`. containing global variables

**default_transformer_type_4_string**:  str (.py), optional, default `One-Hot`. Specify the default `transformer_type` for `dtype='string'`. Options include `One-Hot`, `LabelEncoding`, `Cat1`.

**default_datetime_format**:  str (.py), optional, default `%Y-%m-%d %H:%M:%S`. Specify the default datetime format to use.

**var_list**: list, optional, default `None`. List of variables to transform, to limit the number of transformed variables to a subset of the given inputs. If `None`, all variables will be transformed.

**removeNull**: boolean, default `False`. Whether to remove all rolls with null inputs before transformation.

**debug**: boolean, default `False`. Whether to print debug-related outputs to console.

### Notes

#### Description of metaData
The `metaData` variable specifies the type of transformation to perform on the input data. It takes the following form:
```
metaData = {
    '<variable_name_1>': {
        'null': '33',
        'transformer_type': 'LabelEncoding'
        'datetime_format': None,
    },
    '<variable_name_2>': {
        'null': 'mean'
    },
    'variable_name_datetime': {
        'null': 'mean',
        'datetime_format': f"%Y-%m-%d %H:%M:%S"
    }
}
```

* **null**: use this field to specify the fill value for `<na>` entries. non-numerical options include `'mean'`, `'mode'`, `'median'`, `'ignore'` (left as it is). Numerical values will be used directly. Default for `'boolean'` is -1. Default for `'float'` and `'int'` is `'mean'`. (rounded to `int` for `'int'`)
  * Effects on other packages: With the `'ignore'` option, the marginal distribution will be computed after removing `NaN` values. The pairwise correlation will be computed after removing `NaN` values present in the two variables.
* **transformer_type**: use this field to specify transformer type to use, especially for dtype inputs with multiple options. 
  * For `'string'` inputs, options include `'One-Hot'`, `'LabelEncoding'`, `'Cat1'`, `'Cat1Fuzzy'`
    * *One-Hot*: This option takes in a single column with `N` unique categories and returns `N` vectors, each with a length equal to the length of the original vector. The returned vectors have `1`s in the rows where the corresponding category is found in the original vector and `0`s on the rest.
    * *LabelEncoding*: This option takes in a column of categories and returns a list of the same length with each category replaced by a unique integer representation. The integer value assigned to each category is determined by the order that the categories appear in the input list.
    * *Cat1*: This option computes a representative float for each of the categories found in the fit data. The representatives are computed by sorting the categorical values by their relative frequency, then dividing the `[0, 1]` interval into sub-intervals of lengths corresponding to the relative frequencies and assigning the midpoint of each sub-interval to the corresponding category. When the transformation is reverted, each value is assigned the category that corresponds to the interval it falls in.
    * *Cat1Fuzzy*: This option is the same as *Cat1*, except for the additional Gaussian noise around the class representative of each interval.
* **datetime_format**: use this field to specify the datetime format, for 'datetime' inputs 

### Examples
Please refer to the below pages for detailed examples:

| Example         | Description | 
| ---:              |    :----   |
| [Transformer](../../../gettingStarted/examples/Transformer) | Demonstrates use of Transformer to transform data into its numerical equivalents. |

### Attributes

| Attribute         | Description | 
| ---:              |    :----   |
| debug | (boolean) whether to debug or not  |
| definitions |  (obj) definitions in corresponding input `defintions.py` |
| metaData | (dict) dictionary specifying transformation instructions for specific variables. |
| removeNull | (boolean) Whether to remove all rolls with null inputs before transformation.  |
| var_list | (list) List of variables to transform. |
| data_curated_df | (dataframe) the dataframe that has undergone curation based on `var_list` and `removeNull` options, prior to transformation. |
| default_transformer_type_4_string | (str) the default `transformer_type` for `dtype='string'` |
| default_datetime_format | (str) the default datetime format to use.
| transformer_meta_dict | (dict) dictionary that records all the transformation details effected on the variables.


### Methods

| Method         | Description | 
| ---:              |    :----   |
| transform(data_df) | Perform a numerical transformation on input `data_df`. Transformation details are stored in `Transformer.transformer_meta_dict`. |
| reverse(data) | Perform the reverse transform on the input `data` (dataframe) using `Transformer.transformer_meta_dict` learned during the forward transform |