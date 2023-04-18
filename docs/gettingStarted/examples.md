---
layout: default
title: Examples
parent: Getting Started
nav_order: 5
---

## Example of Transformer Class
This example demonstrates the use of the Transformer class.

### Import Libraries
```
# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)
```

### Generate random data
We're using the `gen_randomData` function to simulate common encountered datatypes, including booleans, floats, integers, date-times, and strings. For greater authenticity, the data contains randomised missing values.
```
# GENERATE RANDOM DATA
dtypes = ['bool', 'float', 'int', 'datetime', 'str', 'str', 'str'] # dtypes
nans = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4] #percentage of nans
size = 12 #number of sample points

rawData_df = gen_randomData(dtypes=dtypes, nans=nans, size=size)
print(f"RAW DATA\n:{rawData_df}")
```

#### Sample output
```
RAW DATA
:   1_bool    2_float  3_int          4_datetime 5_str 6_str 7_str
0    True  64.965030   65.0                 NaT     B     A     D 
1    True  43.137312   63.0                 NaT   NaN     A     C 
2    True  77.959531    NaN 2021-04-30 06:02:00     B   NaN     A 
3     NaN        NaN   22.0 2020-06-05 02:56:00   NaN     C     D 
4   False  74.010448    NaN                 NaT     B   NaN     C 
5   False  43.232770   30.0 2021-07-22 03:09:00   NaN   NaN   NaN 
6    True  78.903848    1.0 2021-08-26 05:19:00     A     C   NaN 
7     NaN  64.350496    NaN                 NaT     B     D   NaN 
8   False        NaN   93.0 2020-09-21 14:34:00     C     A   NaN 
9     NaN        NaN   90.0 2020-03-25 16:31:00     C     B     A 
10    NaN   8.232522    NaN 2021-01-13 19:56:00   NaN   NaN     B 
11  False        NaN   89.0 2021-06-26 17:25:00     D     C     A 
```


```
# DEFINE METADATA SETTINGS FOR Transformer
metaData = {
    '2_float': {
        'null': '33'
    },
    '3_int': {
        'null': 'mean'
    },
    '4_datetime': {
        'null': 'mean',
        'datetime_format': f"%Y-%m-%d %H:%M:%S"
    },
    '5_str': {
        'transformer_type': 'LabelEncoding'
    },
    '6_str': {
        'transformer_type': 'Cat1'
    },
    '7_str': {
        'transformer_type': 'One-Hot'
    }
}

# TRANSFORM THE DATA into a dataframe of floats.
transformer = Transformer(metaData=metaData, debug=False) #initiaise the Transformer with the metaData
numeric_df = transformer.transform(rawData_df)
print(f"TRANSFORMED DATA\n:{numeric_df}")

# REVERTING DATAPOINTS TO ORIGINAL FORMAT
reversed_df = transformer.reverse(numeric_df)
print(f"REVERSED DATA\n:{reversed_df}")
```