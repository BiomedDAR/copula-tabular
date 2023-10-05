import numpy as np
import pandas as pd
from scipy import stats
import os
import platform
import contextlib
import copy
import math


EPSILON = np.finfo(np.float32).eps
OS_TYPE = platform.system()

@contextlib.contextmanager
def random_seed(seed):
    """Context manager for managing the random seed.
    Args:
        seed (int):
            The random seed.
    """

    state = np.random.get_state()
    np.random.seed(seed)
    try: 
        yield
    finally:
        np.random.set_state(state)


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

def gen_dict_range_interval(interval=10,min_num=0,max_num=100):
    import math
    
    # initialise empty dict
    a_dict = {}

    # calc no. of intervals
    num_intervals = math.ceil((max_num - min_num)/interval)
    num_intervals = int(num_intervals)

    # loop through each interval
    for i in range(1, num_intervals+1):
        # calculate the lower and upper bounds of the interval
        lower_bound = min_num + (i-1)*interval
        upper_bound = min(min_num + i*interval, max_num)

        # create a list of the bounds as strings
        if (lower_bound==min_num):
            bounds_list = [">=" + str(lower_bound), "<=" + str(upper_bound)]
        else:
            bounds_list = [">" + str(lower_bound), "<=" + str(upper_bound)]

        # add the interval number and bounds list to the dictionary
        a_dict[i] = bounds_list

    # return the dictionary
    return a_dict

# LINEAR FUNCTIONS
def gen_linear_func(x, m=1, c=0, noise_factor=0):
    noise = stats.uniform.rvs(size=len(x))
    return m*x + c + noise*noise_factor

# BUILD DATA DICTIONARY
def build_basic_data_dictionary(varList, descr="No description available", type="numeric", specific_data_type="float", codings=None, frequency=None, category=None, secondary=None, constraints=None, remarks=None):

    if codings is None: codings = ""
    if category is None: category = ""
    if secondary is None: secondary = ""
    if constraints is None: constraints = ""

    default_dict = {
        "DESCRIPTION": descr,
        "TYPE": type,
        "SPECIFIC DATA TYPE": specific_data_type,
        "CODINGS": codings,
        "FREQUENCY": frequency,
        "CATEGORY": category,
        "COLUMN_NUMBER": 0,
        "SECONDARY": secondary,
        "CONSTRAINTS": constraints,
        "REMARKS": remarks
    }

    # Initialise data_dict
    data_dict = {}
    for var in varList:
        data_dict[var] = default_dict

    # Create Dataframe
    names = list(data_dict.keys())
    values = list(data_dict.values())
    df = pd.DataFrame().from_records(values, columns=list(data_dict[names[0]].keys()))
    df.insert(0, 'NAME', names)

    # Update "COLUMN_NUMBER"
    for index, row in df.iterrows():
        # Set the value of the 'COLUMN_NUMBER' column to be one higher than the row's index
        df.loc[index, 'COLUMN_NUMBER'] = index + 1

    return df



# GENERAL FUNCTIONS FOR FILES
def get_extension(filename):
  return filename.split(".")[-1]

def change_extension(filename, ext):
    file_split = filename.split(".")
    file_split[-1] = ext
    return ".".join(file_split)

def check_filename(file_name):
    """Check if file_name exists"""
    if os.path.exists(file_name):
        return True
    else:
        return False
    
def update_filename_with_suffix(filename, suffix):

    ext = "." + get_extension(filename)
    new_filename = filename.replace(ext, '-' + suffix + ext)

    return new_filename

def clean_filename_str(filename):
    filename = str(filename).replace(":",r"-")
    filename = filename.replace(" ",r"-")

    return filename


# GENERAL FUNCTIONS FOR EXCELS
def get_worksheet_names(file_name):
    '''
    This function takes an Excel workbook filename and returns a list of sheet names
    '''
    # Import pandas
    import pandas as pd
    
    # Read the Excel file
    xl_file = pd.ExcelFile(file_name)
    
    # Return the sheet names
    return xl_file.sheet_names


# GENERAL FUNCTIONS FOR DATAFRAME
def save_df_as_csv(df, filename, index=True):
    df.to_csv(filename, index=index, header=True)

def save_df_as_excel(df, excel_file_name, sheet_name='Sheet1', index=True):
    try:
        with pd.ExcelWriter(path=excel_file_name, engine='auto', mode='w') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
    except Exception as e:
        print(f"Error writing to Excel File: {e}")

def strip_empty_spaces(dataframe):
    dataframe.columns = dataframe.columns.str.strip()
    return dataframe

def strip_string_spaces(dataframe, col=None):

    if col is None:
        for i in range(0, len(dataframe)):
            dataframe[i] = dataframe[i].strip()
    else:
        dataframe[col] = dataframe[col].str.strip()

    return dataframe

def convert_datatypes(df):
    """Convert from nullable datatypes to non-nullable, for backwards compatibility (if required)"""
    for col in df.columns:
        if df[col].dtype == 'Float64':
            df[col] = df[col].astype('float64')
        elif df[col].dtype == 'Int32':
            df[col] = df[col].astype('int32')
        elif df[col].dtype == 'Int64':
            df[col] = df[col].astype('int64')
        else:
            pass
    return df

def df_sampling(df, p=0.8):
    """This function takes in a Pandas dataframe object and a sampling probability `p` and returns two separate dataframes, a sample and a control.
    
    Parameters: 
        df (pandas.Dataframe): A Pandas dataframe object to be sampled.
        p (float): A float value between 0 and 1 representing the sampling probability. Should be less than or equal to 1. This will be used to decide how many rows to be sampled from the original dataframe.

    Returns:
        df_sampled (pandas.Dataframe): A dataframe consisting of randomly-sampled rows from the original dataframe
        df_control (pandas.Dataframe): A dataframe consisting of the remaining rows from the original dataframe
    """
    
    n = df.shape[0]
    s = np.random.choice(n, int(n*p), replace=False)

    df_sampled = df.iloc[s]
    df_control = df[~df.index.isin(s)]

    return df_sampled, df_control


def update_dataframe_rows(df, refCol, listRows, col, val):
    """This function is used to update rows of a dataframe based on certain conditions. 

    Parameters:
        df (dataframe): the dataframe to be updated
        refCol (str): column name of the dataframe to be used as reference for the update
        listRows (list): a list of values from the reference column to determine which rows should be updated
        col (str): column name of the dataframe to be updated
        val (any): new value to be used for updating

    Returns:
        dataframe with updated rows

    Example:

    Assuming a dataframe with columns 'A' and 'B', and columns A consists of values 1,2,3,4

    update_dataframe_rows(df, 'A', [2,4], 'B', 5)

    This will update all the rows with A values of 2 and 4, setting the corresponding B values to 5.
    """

    # update the 'col' column of the dataframe with 'val'
    df.loc[df[refCol].isin(listRows), col] = val

    return df


def mapping_dictDateFormatConversion(str):

    if ("dddd" in str): # day of the week, full form (Monday):
        str = str.replace("dddd", r"%A")

    if ("ddd" in str): # day of the week, short form (Mon):
        str = str.replace("ddd", r"%a")

    if ("dd" in str): # day number with a leading zero
        str = str.replace("dd", r"%d")
    elif ("d" in str): # day number without a leading zero
        if OS_TYPE=='Windows': # use "%-d" for unix, "%#d" for windows
            str = str.replace("d", r"%#d")
        elif OS_TYPE=='Linux' or 'Darwin':
            str = str.replace("d", r"%-d")

    if ("mmmm" in str): # month name, full form, (January):
        str = str.replace("mmmm", r"%B")

    if ("mmm" in str): # month name, short form, (Jan):
        str = str.replace("mmm", r"%b")

    if ("mm" in str): # month number with a leading zero
        str = str.replace("mm", r"%m")
    elif ("m" in str): # month number without a leading zero
        if OS_TYPE=='Windows': # use "%-m" for unix, "%#m" for windows
            str = str.replace("m", r"%#m")
        elif OS_TYPE=='Linux' or 'Darwin':
            str = str.replace("m", r"%-m")
    
    if ("yyyy" in str): # year four digits
        str = str.replace("yyyy", r"%Y")

    if ("yy" in str): # year last 2 digits
        str = str.replace("yy", r"%y")

    return str

# TIME
def date_format_search(data):
    list_of_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%m/%d/%Y", "%d/%m/%Y", "%d.%m.%Y", "%d %B %Y", "%b %d, %Y", "%y-%m-%d", "%d-%m-%y", "%m-%d-%y", "%m/%d/%y", "%d/%m/%y", "%d.%m.%y", "%d %B %y", "%b %d, %y"]

    chosen_format = list_of_formats[0]
    num_NaT = len(data)
    for format in list_of_formats:
        num_Nat_i = count_date_format_errors(data, format)
        if num_Nat_i < num_NaT:
            num_NaT = num_Nat_i
            chosen_format = format

    return chosen_format

def count_date_format_errors(data, format):

    data = strip_string_spaces(data)
    con_data = pd.to_datetime(data, format=format, errors="coerce")
    num_NaT = con_data.isnull().sum()

    return num_NaT

# ASCII-compatible
def convert_to_ascii(data):
    """
    Function to convert all string/object columns in a dataframe to characters that can safely be encoded to ASCII.
    """
    # load unidecode package
    from unidecode import unidecode
  
    # Iterate through columns of the dataframe
    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            # Select only string/object columns
            if data[col].dtype == object or data[col].dtype == "string":
                # Remove international accents from the column and assign it back to the same column
                data[col] = data[col].apply(unidecode)
                # data[col] = data[col].str.replace("€", r"\€", regex=True).apply(unidecode)
    elif type(data) == str:
        data = unidecode(data)
    
    return data


# GENERAL ALGORITHMS
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

def remove_items(listA, listB):
  """Removes the items in list A from list B."""
  for item in listA:
    if item in listB:
      listB.remove(item)
  return listB

# LINEAR ALGEBRA
def is_pos_def(A):
    """Check if symmetric matrix is positive definite"""
    if np.allclose(A, A.T):
        try:
            np.linalg.cholesky(A)
            return True
        except np.linalg.LinAlgError:
            return False
    else:
        # NOT SYMMETRIC
        return False
    
def makePD(corr):
    """Convert a matrix to positive definite"""
    if (is_pos_def(corr)):
        return corr
    else:
        eigValue, eigVector = np.linalg.eigh(corr)
        cnvEigV = np.diag(np.clip(eigValue, EPSILON, 100000))
        new_corr = eigVector @ cnvEigV @ eigVector.transpose()
        Norm = np.tile(np.diag(new_corr),(np.diag(new_corr).size,1))
        new_corr = np.divide(new_corr,np.sqrt(Norm*Norm.transpose()))

        return new_corr
    
