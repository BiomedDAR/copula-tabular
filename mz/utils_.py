import numpy as np
import pandas as pd

def gen_randomData(
    dtypes = ['bool','bool','float', 'int', 'str'],
    nans = 0,
    size = 10,
    baseline_date = '2019-10-13T18:34',
):
    """Generate random dataset
        Input:
            dtypes(list): list of dtypes, e.g. ['bool', 'float', 'int', 'str']
            nans(float, list): list of floats in [0,1]. Designate the proportion of nans. Default is 0.
            size(int): no. of samples. Default is 10.
            baseline_date (str): baseline data for generating random datetimes. Default is '2019-10-13T18:34', with format %Y-%m-%d %H:%M:%S.
        Output: data_df (dataframe)
        """
    columns = {}

    if np.isscalar(nans):
        nans = [nans] * len(dtypes)

    for count, (dtype, nan) in enumerate(zip(dtypes, nans), start=1):

        if dtype == 'bool':
            column = np.random.choice([True, False], size=size)
        if dtype == 'float':
            column = np.random.random(size) * 100
        if dtype == 'int':
            column = np.random.randint(100, size=size)
        if dtype == 'str':
            column = np.random.choice(['A', 'B', 'C', 'D'], size=size)
        if dtype == 'datetime':
            deltas = np.random.randint(1000000, size=size)
            datetimes = np.array([np.datetime64(baseline_date)] * size)
            column = datetimes + deltas

        column = pd.Series(column)
        
        # Add in NANs
        nan_index = np.random.choice(
            range(size), 
            size=int(size * nan), 
            replace=False
        )
        column.iloc[nan_index] = np.nan

        columns[f'{count}_{dtype}'] = column
    
    data_df = pd.DataFrame(columns)
    return data_df


# GENERAL
def gcd(x):
    """Find the Greatest Common Divisor of a dataframe column"""
    x = x.dropna().reset_index(drop=True)
    a = x[0] #initialize a with the first element of the list
    for i in range(1, len(x)): 
        b = x[i] #initialize b with the next element of the list
        while b != 0: 
            c = b 
            b = a % b 
            a = c 
    return a 