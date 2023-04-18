from copy import deepcopy
import pandas as pd
import os
import numpy as np

from mz import utils_ as ut_

class Transformer:
    """
    Inputs:
        metaData (dict): 
            E.g. '<name of field>: {
                'null': use this field to specify the fill value for <na> entries. non-numerical options include 'mean', 'mode', 'median'. Numerical values will be used directly. Default for 'boolean' is -1. Default for 'float' and 'int' is 'mean'. (rounded to int for 'int')
                'transformer_type': use this field to specify transformer type, esp. for 'string' inputs. Options include 'One-Hot', 'LabelEncoding', 'Cat1'
                'datetime_format': use this field to specify the datetime format, for 'datetime' inputs
            }
    """
    def __init__(self,
        metaData=None,
        definitions=None,
        debug=True
    ):
        self.metaData = metaData
        self.definitions = definitions
        self.debug = debug
        self.transformer_meta_dict = None

        self.default_transformer_type_4_string = 'One-Hot'

    def convert_2_dtypes(self, data):
        """Convert data (df) into best possible dtypes"""
        return data.convert_dtypes()
    
    def _get_null_value_from_metaData(self, column, default_value, data_df):
        """Compute the set_null_value from options specified in metaData for the field: column"""

        set_null_value = default_value
        if self.metaData is not None:
            if column in self.metaData:
                if 'null' in self.metaData[column]:
                    null_value = self.metaData[column]['null']

                    if (null_value=='mean'):
                        set_null_value = data_df[column].mean()
                    elif (null_value=='mode'):
                        set_null_value = data_df[column].mode(dropna=True)[0]
                    elif (null_value=='median'):
                        set_null_value = data_df[column].median()
                    else:
                        set_null_value = float(null_value)
        
        return set_null_value
    
    def _get_datetime_format_from_metaData(self, column):

        datetime_format = None
        if self.metaData is not None:
            if column in self.metaData:
                if 'datetime_format' in self.metaData[column]:

                    datetime_format = self.metaData[column]['datetime_format']

        return datetime_format
    
    def _get_transformer_type_from_metaData(self, column, data_df):

        # set defaults based on dtype
        col_dtype_str = data_df[column].dtype
        if col_dtype_str=='string':
            transformer_type = self.default_transformer_type_4_string

        if self.metaData is not None:
            if column in self.metaData:
                if 'transformer_type' in self.metaData[column]:
                    transformer_type = self.metaData[column]['transformer_type']

        return transformer_type
    
    def _categorical_transformer(self, df_col):

        # Create a dictionary to store the relative frequences of each category
        rel_freq = {}

        # Calculate the relative frequencies of each category
        for cat in df_col.unique():
            
            cat_count = df_col[df_col==cat].count() # count the no. of times the cat appears
            rel_freq[cat] = cat_count/df_col.count() # compute relative freq. of the category

        # Sort the categories by their relative frequencies
        sorted_categories = {}
        for k,v in sorted(rel_freq.items(), key=lambda x:x[1]):
            sorted_categories[k] = v

        # Divide the [0,1] interval by the relative frequencies
        cat_intervals = {}
        intervals = []
        lower_bound = 0
        for cat in sorted_categories:
            upper_bound = lower_bound + rel_freq[cat]
            intervals.append([lower_bound, upper_bound])
            cat_intervals[cat] = [lower_bound, upper_bound]
            lower_bound = upper_bound
            

        # Assign the middle point of each interval to the corresponding category
        rep = {}
        for i, cat in enumerate(sorted_categories):
            rep[cat] = (intervals[i][0] + intervals[i][1]) / 2
        
        # Replace the instances of the categories with the corresponding representative
        transformed_column = deepcopy(df_col)
        for cat in df_col.unique():
            transformed_column[df_col==cat] = rep[cat]

        transformed_column = transformed_column.astype('float') #convert column from uint8 to float dtype

        return transformed_column, rep, cat_intervals
    
    def _reverse_categorical_transformer(self, df_col, intervals):
        
        df_col = df_col.clip(0, 1)
        rev_df_col = df_col.apply(lambda x: next(key for key, (lower, upper) in intervals.items() if lower <= x <= upper))
                                  
        return rev_df_col
    
    def transform(self, data_df):

        # initialise empty dataframe
        numeric_df = pd.DataFrame()
        transformer_meta_dict = {}

        # convert data_df to best possible dtypes
        data_df = self.convert_2_dtypes(data_df)

        # loop through each column of the dataframe 
        for i, col in enumerate(data_df.columns):

            transformer_meta_dict[col] = {} #initialise transformer_meta_dict for field
            
            # GET PANDAS dtype for column i
            col_dtype_str = data_df[col].dtype
            transformer_meta_dict[col]['original_dtype'] = col_dtype_str #update transformer_meta_dict with original pd dtype of field

            if (self.debug):
                print(f"Transforming column {i}: {col} of type {col_dtype_str}")

            # TRANSFORMING
            
            # (1) BOOLEAN / NUMERICAL (float64)/(int64)
            if (col_dtype_str=='boolean' or col_dtype_str=='Float64' or col_dtype_str=='Int64'):
                output_field_name = f"{col}.value"

                numeric_df[output_field_name] = data_df[col].astype(float)

                if (col_dtype_str=='boolean'):
                    transformer_meta_dict[col]['transformer_type'] = 'Boolean'
                elif (col_dtype_str=='Float64'):
                    transformer_meta_dict[col]['transformer_type'] = 'Numerical'
                elif (col_dtype_str=='Int64'):
                    transformer_meta_dict[col]['transformer_type'] = 'Numerical-INT'

                transformer_meta_dict[col]['output_fields'] = {
                    output_field_name: {
                        'dtype': numeric_df[output_field_name].dtype  # update transformer_meta_dict with output pd dtype of field
                    }
                }
            elif (col_dtype_str=='datetime64[ns]'):

                # Extract datetime_format from metaData
                datetime_format = self._get_datetime_format_from_metaData(column=col)

                # Convert from string/datetime to pandas datetime format
                output_field_name = f"{col}.value"
                numeric_df[output_field_name] = pd.to_datetime(data_df[col], format=datetime_format)

                # Convert column from datetime to int format
                null_mask = numeric_df[output_field_name].isnull()
                numeric_df[output_field_name] = numeric_df[output_field_name].astype(np.int64)
                numeric_df[output_field_name] = numeric_df[output_field_name].mask(null_mask, np.nan)

                # Find smallest denominator by applying GCD function to dataframe column
                gcd = ut_.gcd(numeric_df[output_field_name])

                # Reduce converted datetime by GCD
                numeric_df[output_field_name] = numeric_df[output_field_name] // gcd
                numeric_df[output_field_name] = numeric_df[output_field_name].astype(float)

                # Update meta_dict
                transformer_meta_dict[col]['transformer_type'] = 'Datetime'
                transformer_meta_dict[col]['datetime_format'] = datetime_format
                transformer_meta_dict[col]['common_divider'] = gcd
                transformer_meta_dict[col]['output_fields'] = {
                    output_field_name: {
                        'dtype': numeric_df[output_field_name].dtype  # update transformer_meta_dict with output pd dtype of field
                    }
                }

            elif (col_dtype_str=='string' or col_dtype_str=='object' or col_dtype_str=='category'):

                transformer_type = self._get_transformer_type_from_metaData(col, data_df)

                if transformer_type=='One-Hot':
                    # Perform one-hot encoding
                    df_onehot = pd.get_dummies(data_df[col], prefix=col, prefix_sep='.')
                    numeric_df = pd.concat([numeric_df, df_onehot], axis=1)
                    numeric_df = numeric_df.astype('float') #convert column from uint8 to float dtype

                    # Update meta_dict
                    transformer_meta_dict[col]['transformer_type'] = 'One-Hot'
                    transformer_meta_dict[col]['output_fields'] = {}
                    for onehotcol in df_onehot.columns:
                        transformer_meta_dict[col]['output_fields'][onehotcol] = {
                            'dtype': numeric_df[onehotcol].dtype  # update transformer_meta_dict with output pd dtype of field
                        }
                elif transformer_type=='LabelEncoding':
                    # Perform label encoding

                    data_df[col] = data_df[col].fillna('IS_NULL')
                    
                    # Create a dictionary to map each string to its corresponding integer 
                    dic = {x[1]:x[0] for x in enumerate(set(data_df[col]))}
                    inv_dic = {x[0]:x[1] for x in enumerate(set(data_df[col]))}
                    
                    # Use the dictionary to map each string to its corresponding integer
                    output_field_name = f"{col}.value"
                    numeric_df[output_field_name] = data_df[col].map(dic).astype('float')

                    # Update meta_dict
                    transformer_meta_dict[col]['transformer_type'] = 'LabelEncoding'
                    transformer_meta_dict[col]['params_dict'] = dic
                    transformer_meta_dict[col]['inv_params_dict'] = inv_dic
                    transformer_meta_dict[col]['output_fields'] = {
                        output_field_name: {
                            'dtype': numeric_df[output_field_name].dtype  # update transformer_meta_dict with output pd dtype of field
                        }
                    }

                elif transformer_type=='Cat1':
                    # Categorical transformation: assigning representative float by frequency of occurence
                    data_df[col] = data_df[col].fillna('IS_NULL')
                    output_field_name = f"{col}.value"
                    transformed_col, rep, intervals = self._categorical_transformer(data_df[col])
                    numeric_df[output_field_name] = transformed_col

                    # Update meta_dict
                    transformer_meta_dict[col]['transformer_type'] = 'Cat1'
                    transformer_meta_dict[col]['params_dict'] = rep
                    transformer_meta_dict[col]['intervals'] = intervals
                    transformer_meta_dict[col]['output_fields'] = {
                        output_field_name: {
                            'dtype': numeric_df[output_field_name].dtype  # update transformer_meta_dict with output pd dtype of field
                        }
                    }

                else:
                    raise TypeError('Transformer Type is not recognised.')
            else:
                raise TypeError('Input array must be of type boolean, Float64, Int64, string')

            # FIX NULLS (not used for categorical)
            fix_null = False
            got_null = data_df[col].isna().any()
            if got_null:
                fix_null = True

                null_output_field_name = f"{col}.is_null" #follow convention in SDV
                numeric_df[null_output_field_name] = data_df[col].isna().astype(float)

                transformer_meta_dict[col]['output_fields'][null_output_field_name] = {
                    'dtype': numeric_df[null_output_field_name].dtype  # update transformer_meta_dict with output pd dtype of field
                }

                if (col_dtype_str=='boolean'):
                    set_null_value = self._get_null_value_from_metaData(
                        column = col,
                        default_value = -1, #default fill value for boolean is set to -1
                        data_df = data_df
                    )
                    numeric_df.loc[data_df[col].isna(), output_field_name] = set_null_value
                elif (col_dtype_str=='Float64'):
                    set_null_value = self._get_null_value_from_metaData(
                        column = col,
                        default_value = data_df[col].mean(), #default fill value for float is set to mean
                        data_df = data_df
                    )
                    numeric_df.loc[data_df[col].isna(), output_field_name] = set_null_value
                elif (col_dtype_str=='Int64'):
                    set_null_value = self._get_null_value_from_metaData(
                        column = col,
                        default_value = data_df[col].mean(), #default fill value for int is set to mean
                        data_df = data_df
                    )
                    numeric_df.loc[data_df[col].isna(), output_field_name] = round(set_null_value)
                elif (col_dtype_str=='datetime64[ns]'):
                    set_null_value = self._get_null_value_from_metaData(
                        column = f"{col}.value",
                        default_value = numeric_df[f"{col}.value"].mean(), #default fill value for datetime is set to mean
                        data_df = numeric_df
                    )
                    numeric_df.loc[data_df[col].isna(), output_field_name] = round(set_null_value)

            transformer_meta_dict[col]['null'] = {
                'got_null': got_null,
                'fix_null': fix_null,
            }

        self.transformer_meta_dict = transformer_meta_dict

        return numeric_df


    def reverse(self, data):

        # initialise empty dataframe
        revert_df = pd.DataFrame()

        # loop through every transformed field
        for field, field_meta in self.transformer_meta_dict.items():

            # get output fields
            output_fields_dict = field_meta['output_fields']
            for output_field_name, output_field_meta in output_fields_dict.items():

                # IF BOOLEAN
                if (field_meta['original_dtype']=='boolean'):
                    if output_field_name == (f"{field}.value"):
                        revert_df[field] = np.round(data[output_field_name]).clip(0, 1).astype('boolean')
                # IF FLOAT
                elif (field_meta['original_dtype']=='Float64'):
                    if output_field_name == (f"{field}.value"):
                        revert_df[field] = data[output_field_name]
                # IF INT
                elif (field_meta['original_dtype']=='Int64'):
                    if output_field_name == (f"{field}.value"):
                        revert_df[field] = np.round(data[output_field_name])
                # IF DATETIME
                elif (field_meta['original_dtype']=='datetime64[ns]'):
                    if output_field_name == (f"{field}.value"):
                        revert_df_col = data[output_field_name] * field_meta['common_divider']
                        revert_df_col = pd.to_datetime(revert_df_col)
                        revert_df[field] = revert_df_col.dt.strftime(field_meta['datetime_format'])
            # IF STRING
            if (field_meta['original_dtype']=='string'):
                if (field_meta['transformer_type']=='One-Hot'):

                    # Get column names 
                    column_names = list(output_fields_dict.keys())
                    decoded_df = data[column_names].idxmax(axis=1)
                    revert_df[field] = decoded_df.str.split('.').str[1]
                    revert_df[field].replace('is_null', np.nan, inplace=True)

                if (field_meta['transformer_type']=='LabelEncoding'):

                    # Get dic from field_meta
                    dic = field_meta['inv_params_dict']

                    # Use the dictionary to reverse the label encoding
                    revert_col = data[output_field_name].clip(min(dic),max(dic))
                    revert_df[field] = revert_col.round().map(dic)
                    revert_df[field].replace('IS_NULL', np.nan, inplace=True)

                elif (field_meta['transformer_type']=='Cat1'):

                    # Get interval dict from field_meta
                    intervals = field_meta['intervals']
                    revert_df[field] = self._reverse_categorical_transformer(data[output_field_name], intervals)
                    revert_df[field].replace('IS_NULL', np.nan, inplace=True)

            # FIX NULL for non-string inputs
            if (field_meta['original_dtype']!='string'):
                # identify null cells
                if (field_meta['null']['fix_null']):
                    isnull = data[f"{field}.is_null"] > 0.5
                # set identified null cells to nan
                if (field_meta['null']['fix_null']):
                    revert_df.loc[isnull, field] = np.nan

        return self.convert_2_dtypes(revert_df)