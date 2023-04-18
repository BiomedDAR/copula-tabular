# This example demonstrates the use of the Transformer class.

# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from mz.Transformer import Transformer #import Transformer class
from mz.utils_ import gen_randomData #import random data generator

# GENERATE RANDOM DATA
dtypes = ['bool', 'float', 'int', 'datetime', 'str', 'str', 'str', 'str'] # dtypes
nans = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4] #percentage of nans
size = 12 #number of sample points

rawData_df = gen_randomData(dtypes=dtypes, nans=nans, size=size)
print(f"RAW DATA\n:{rawData_df}")

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

# TRANSFORM THE DATA into a dataframe of floats.
transformer = Transformer(metaData=metaData, debug=False) #initiaise the Transformer with the metaData
numeric_df = transformer.transform(rawData_df)
print(f"TRANSFORMED DATA\n:{numeric_df}")

# REVERTING DATAPOINTS TO ORIGINAL FORMAT
reversed_df = transformer.reverse(numeric_df)
print(f"REVERSED DATA\n:{reversed_df}")