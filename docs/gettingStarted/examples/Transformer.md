---
layout: default
title: Example for Transformer class
parent: Examples
grand_parent: Getting Started
nav_order: 1
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
dtypes = ['bool', 'float', 'int', 'datetime', 'str', 'str', 'str', 'str'] # dtypes
nans = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4] #percentage of nans
size = 12 #number of sample points

rawData_df = gen_randomData(dtypes=dtypes, nans=nans, size=size)
print(f"RAW DATA\n:{rawData_df}")
```

#### Sample output
```
RAW DATA
:   1_bool    2_float  3_int          4_datetime 5_str 6_str 7_str 8_str
0   False   7.058297   42.0 2019-12-26 06:39:00     D   NaN     D   NaN 
1   False  13.122099   71.0                 NaT     A     A     D   NaN 
2     NaN        NaN   26.0                 NaT     C     C     D     B 
3     NaN  89.938102    NaN 2020-06-09 07:08:00     C     B     A   NaN 
4    True  85.527006    NaN 2020-02-22 12:54:00     C     B     D     A 
5     NaN  72.566412   39.0 2020-06-04 08:36:00   NaN   NaN     A     B 
6   False  30.504605    NaN                 NaT   NaN     C     D     D 
7     NaN  63.675184    NaN                 NaT     D     A     C     C 
8    True        NaN   11.0 2021-07-05 12:22:00     A     A   NaN     B 
9    True        NaN   95.0 2021-05-15 06:56:00     C   NaN   NaN     C 
10  False  75.161072   36.0 2020-02-17 00:23:00   NaN     C   NaN     C 
11  False        NaN   60.0 2021-08-10 22:58:00   NaN   NaN   NaN   NaN
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
    },
    '8_str': {
        'transformer_type': 'Cat1Fuzzy'
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
:    1_bool.value  1_bool.is_null  2_float.value  2_float.is_null  3_int.value  3_int.is_null  4_datetime.value  4_datetime.is_null  5_str.value  6_str.value  7_str.A  7_str.C  7_str.D  7_str.is_null  8_str.value
0            0.0             0.0       7.058297              0.0         42.0            0.0        26289039.0                 0.0          1.0     0.166667      0.0      0.0      1.0            0.0     0.081037 
1            0.0             0.0      13.122099              0.0         71.0            0.0        26666144.0                 1.0          2.0     0.458333      0.0      0.0      1.0            0.0     0.119631 
2           -1.0             1.0      33.000000              1.0         26.0            0.0        26666144.0                 1.0          0.0     0.708333      0.0      0.0      1.0            0.0     0.450521 
3           -1.0             1.0      89.938102              0.0         48.0            1.0        26528108.0                 0.0          0.0     0.916667      1.0      0.0      0.0            0.0     0.156109 
4            1.0             0.0      85.527006              0.0         48.0            1.0        26372934.0                 0.0          0.0     0.916667      0.0      0.0      1.0            0.0     0.876966 
5           -1.0             1.0      72.566412              0.0         39.0            0.0        26520996.0                 0.0          3.0     0.166667      1.0      0.0      0.0            0.0     0.417472 
6            0.0             0.0      30.504605              0.0         48.0            1.0        26666144.0                 1.0          3.0     0.708333      0.0      0.0      1.0            0.0     0.964542 
7           -1.0             1.0      63.675184              0.0         48.0            1.0        26666144.0                 1.0          1.0     0.458333      0.0      1.0      0.0            0.0     0.674243
8            1.0             0.0      33.000000              1.0         11.0            0.0        27091462.0                 0.0          2.0     0.458333      0.0      0.0      0.0            1.0     0.452573
9            1.0             0.0      33.000000              1.0         95.0            0.0        27017696.0                 0.0          0.0     0.166667      0.0      0.0      0.0            1.0     0.632900
10           0.0             0.0      75.161072              0.0         36.0            0.0        26364983.0                 0.0          3.0     0.708333      0.0      0.0      0.0            1.0     0.657557
11           0.0             0.0      33.000000              1.0         60.0            0.0        27143938.0                 0.0          3.0     0.166667      0.0      0.0      0.0            1.0     0.100591
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
:    1_bool    2_float  3_int           4_datetime 5_str 6_str 7_str 8_str
0    False   7.058297     42  2019-12-26 06:39:00     D  <NA>     D  <NA>
1    False  13.122099     71                 <NA>     A     A     D  <NA>
2     <NA>       <NA>     26                 <NA>     C     C     D     B
3     <NA>  89.938102   <NA>  2020-06-09 07:08:00     C     B     A  <NA>
4     True  85.527006   <NA>  2020-02-22 12:54:00     C     B     D     A
5     <NA>  72.566412     39  2020-06-04 08:36:00  <NA>  <NA>     A     B
6    False  30.504605   <NA>                 <NA>  <NA>     C     D     D
7     <NA>  63.675184   <NA>                 <NA>     D     A     C     C
8     True       <NA>     11  2021-07-05 12:22:00     A     A  <NA>     B
9     True       <NA>     95  2021-05-15 06:56:00     C  <NA>  <NA>     C
10   False  75.161072     36  2020-02-17 00:23:00  <NA>     C  <NA>     C
11   False       <NA>     60  2021-08-10 22:58:00  <NA>  <NA>  <NA>  <NA>
```