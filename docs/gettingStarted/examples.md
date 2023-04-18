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

### Define metadata settings for Transformer
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
```

### Transform the input data into its numerical representative
```
# TRANSFORM THE DATA into a dataframe of floats.
transformer = Transformer(metaData=metaData, debug=False) #initiaise the Transformer with the metaData
numeric_df = transformer.transform(rawData_df)
print(f"TRANSFORMED DATA\n:{numeric_df}")
```

#### Sample output
```
TRANSFORMED DATA
:    1_bool.value  1_bool.is_null  2_float.value  2_float.is_null  3_int.value  3_int.is_null  4_datetime.value  4_datetime.is_null  5_str.value  6_str.value  7_str.A  7_str.B  7_str.C  7_str.D  7_str.is_null
0            1.0             0.0      64.965030              0.0         65.0            0.0        26852324.0                 1.0          2.0     0.291667      0.0      0.0      0.0      1.0            0.0
1            1.0             0.0      43.137312              0.0         63.0            0.0        26852324.0                 1.0          3.0     0.291667      0.0      0.0      1.0      0.0            0.0
2            1.0             0.0      77.959531              0.0         57.0            1.0        26996042.0                 0.0          2.0     0.833333      1.0      0.0      0.0      0.0            0.0
3           -1.0             1.0      33.000000              1.0         22.0            0.0        26522096.0                 0.0          3.0     0.541667      0.0      0.0      0.0      1.0            0.0
4            0.0             0.0      74.010448              0.0         57.0            1.0        26852324.0                 1.0          2.0     0.833333      0.0      0.0      1.0      0.0            0.0
5            0.0             0.0      43.232770              0.0         30.0            0.0        27115389.0                 0.0          3.0     0.833333      0.0      0.0      0.0      0.0            1.0
6            1.0             0.0      78.903848              0.0          1.0            0.0        27165919.0                 0.0          1.0     0.541667      0.0      0.0      0.0      0.0            1.0
7           -1.0             1.0      64.350496              0.0         57.0            1.0        26852324.0                 1.0          2.0     0.041667      0.0      0.0      0.0      0.0            1.0
8            0.0             0.0      33.000000              1.0         93.0            0.0        26678314.0                 0.0          4.0     0.291667      0.0      0.0      0.0      0.0            1.0
9           -1.0             1.0      33.000000              1.0         90.0            0.0        26419231.0                 0.0          4.0     0.125000      1.0      0.0      0.0      0.0            0.0
10          -1.0             1.0       8.232522              0.0         57.0            1.0        26842796.0                 0.0          3.0     0.833333      0.0      1.0      0.0      0.0            0.0
11           0.0             0.0      33.000000              1.0         89.0            0.0        27078805.0                 0.0          0.0     0.541667      1.0      0.0      0.0      0.0            0.0
```

### Reverse numerical data back to its original form
```
# REVERTING DATAPOINTS TO ORIGINAL FORMAT
reversed_df = transformer.reverse(numeric_df)
print(f"REVERSED DATA\n:{reversed_df}")
```

#### Sample output
```
REVERSED DATA
:    1_bool    2_float  3_int           4_datetime 5_str 6_str 7_str
0     True   64.96503     65                 <NA>     B     A     D
1     True  43.137312     63                 <NA>  <NA>     A     C
2     True  77.959531   <NA>  2021-04-30 06:02:00     B  <NA>     A
3     <NA>       <NA>     22  2020-06-05 02:56:00  <NA>     C     D
4    False  74.010448   <NA>                 <NA>     B  <NA>     C
5    False   43.23277     30  2021-07-22 03:09:00  <NA>  <NA>  <NA>
6     True  78.903848      1  2021-08-26 05:19:00     A     C  <NA>
7     <NA>  64.350496   <NA>                 <NA>     B     D  <NA>
8    False       <NA>     93  2020-09-21 14:34:00     C     A  <NA>
9     <NA>       <NA>     90  2020-03-25 16:31:00     C     B     A
10    <NA>   8.232522   <NA>  2021-01-13 19:56:00  <NA>  <NA>     B
11   False       <NA>     89  2021-06-26 17:25:00     D     C     A
```