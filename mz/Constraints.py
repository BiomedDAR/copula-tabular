from mz import utils_ as ut_
from copy import deepcopy
import pandas as pd

class Constraints:
    """
    """

    def __init__(self,
        debug=False
    ):
        self.debug = debug
        self.log = {}

    def init_log(self, var):
        if var not in self.log:
            self.log[var] = {}

    def multiparent_conditions(self, df, var_array, dict_conditions_values):
        """Function for replacement of values in a dataframe based on multiple conditions evaluated from multiple columns.
        
        Parameters:
            df (dataframe): The dataframe to be updated.
            var_array (list): A list of strings of column names to be updated.
            dict_condiions_values (dict): A dictionary of conditions and values. The conditions are evaluated from multiple columns and the corresponding value is then inserted into the specified columns.
        
        Returns:
            df (dataframe): The updated dataframe

        Example usage: 
            df = multiparent_conditions(df, ["column1", "column2"], 
                {0: {"conditions": {"parent1": {"parent": "parent1_column", "condition": "> 5"}, 
                                    {"parent2": {"parent": "parent2_column", "condition": "< 10"}}, 
                        "value": 0}, 
                1: {"conditions": {"parent3": {"parent": "parent3_column", "condition": "== 'Yes'"}}, 
                    "value": 1 #note that assigned value must match the dtype of column
                    }
                })
        
            This example updates the dataframe with the values 0 and 1 in "column1" and "column2" columns respectively, according to the conditions given. In particular, the value 0 is inserted when "parent1_column" is greater than 5 AND "parent2_column" is less than 10. The value 1 is inserted when "parent3_column" is equal to "Yes".
        """

        # Initialise log
        for var in var_array:
            self.init_log(var)
            df[var] = df[var].convert_dtypes()
        
        # Iterate through conditions and values
        for key, dict_condition_value in dict_conditions_values.items():
            cond_ = True
            for key2, dict_condition in dict_condition_value['conditions'].items():
                parent = dict_condition['parent']
                condition = dict_condition['condition']

                # Evaluate the dataframe column and update the new column
                if isinstance(condition, str):
                    cond_ = cond_ & (df[parent].map(eval(f"lambda x: x{condition}")))
                else:
                    cond_ = cond_ & (df[parent].map(condition))

            df.loc[cond_,var_array] = dict_condition_value['value']

        # Convert dataframe to best possible dtype
        for var in var_array:
            df[var] = df[var].convert_dtypes()

        # Create log
        for var in var_array:
            msg = f"Replaced {var} using conditions and values given in dict_conditions_values."
            self.log[var]['evaluate_df_column'] = msg

            if self.debug:
                print(f"For variable: {var}: {msg}")

        return df


    def evaluate_df_column(self, df, column_names, dict_conditions_values=None, func=None, output_column_name=None):
        """This function takes a dataframe and column name(s) and evaluates the column based on the given conditions and values, creating a new column in the dataframe with the evaluated values. Optionally, a function can be passed in to evaluate the column.

        Parameters:
            df (dataframe): a dataframe object to be evaluated
            column_names (str, list): a string or list of strings containing the name(s) of the columns to be evaluated
            dict_conditions_values (dict): Optional. A dictionary containing the conditions and values to be evaluated. E.g.
                dict_conditions_values = {
                    i : {
                        condition: lambda x: x> 5 # can be given as a string, e.g. "x>5"
                        value: "'5+'"
                    }
                }
            func (function): Optional. A function to be applied on the columns
            output_column_name (str): Optional. A string containing the name of the output column. If not provided, the default is the name of the column plus '_evaluated'.

        Returns:
            df (dataframe): the dataframe with the evaluated values in the new column

        Example usage:
            df = evaluate_df_column(df, 'item', dict_conditions_values=
                {
                    'condition_1': {'condition': 'x == "apples"', 'value': '"fruit"'},
                    'condition_2': {'condition': 'x == "oranges"', 'value': '"fruit"'},
                    'condition_3': {'condition': 'x == "carrots"', 'value': '"vegetable"'},
                    'condition_4': {'condition': 'x == "potatoes"', 'value': '"vegetable"'}
                },
                output_column_name='item_type'
            )
        """
        
        # Create a new column with the new values
        if isinstance(column_names, str):
            if output_column_name is None:
                output_column_name = column_name + '_evaluated'
            df[output_column_name] = df[column_names].copy()
        else:
            column_name = column_names[0]
            if output_column_name is None:
                output_column_name = ''.join(column_names) + '_evaluated'
            df[output_column_name] = df[column_name].copy()

        # initialise log
        self.init_log(output_column_name) 

        if func is None:
            # Iterate through each condition and value
            for i, conditions_values in dict_conditions_values.items():
                condition = conditions_values['condition']
                value = conditions_values['value']

                # Evaluate the dataframe column and update the new column
                if isinstance(column_names, str):
                    if isinstance(condition, str):
                        df.loc[df[column_names].map(eval(f"lambda x: {condition}")), output_column_name] = eval(value)
                    else:
                        df.loc[df[column_names].map(condition), output_column_name] = eval(value)
                else:
                    for column_name in column_names:
                        if isinstance(condition, str):
                            df.loc[df[column_name].map(eval(f"lambda x: {condition}")), output_column_name] = eval(value)
                        else:
                            df.loc[df[column_name].map(condition), output_column_name] = eval(value)

        else:
            # df[output_column_name] = df[column_name].map(lambda x: func(x))
            df[output_column_name] = df.apply(lambda row: func(row[column_names]), axis = 1)

        # Convert dataframe to best possible dtype
        df[output_column_name] = df[output_column_name].convert_dtypes()

        # Create log
        msg = f"Replaced {output_column_name} using conditions and values given in dict_conditions_values."
        self.log[output_column_name]['evaluate_df_column'] = msg

        if self.debug:
            print(f"For variable: {output_column_name}: {msg}")

        return df



    def convertBlankstoValue(self, df, var_array=None, value=None):
        """This function is used to convert missing values in a dataframe column to a specified value.
        
        Parameters:
            df (dataframe): the dataframe containing the variable.
            var_array (list): an array of variable names that need to be processed.
            value (string): the replacement value to be given for missing values. If None, 'UNK' is used as default.

        Returns:
            df (dataframe): the updated dataframe.

        Raises:
            ValueError: if the variable is not found in the given dataframe.

        Example Usage:
            # Load the dataframe
            df = pd.read_csv('data.csv')

            # Create an array of variables
            var_array = ['Var1', 'Var2', 'Var3']

            # Convert missing values in the dataframe to 'UNK'
            convertBlankstoValue(df, var_array, value='UNK')
        """

        for v in var_array:
            if v not in df.columns:
                raise ValueError(f"Variable: {v} not found in given dataframe")
            
            self.init_log(v) # initialise log
            
            # Convert dataframe to best possible dtype
            df[v] = df[v].convert_dtypes()

            # Get dtype of df[v]
            var_dtype = df[v].dtypes

            # Get replace_value
            if value is None:
                if var_dtype=="string":
                    replace_value = "UNK"
            else:
                replace_value = value

            # return the number of missing values converted
            number_of_missing_values_converted = df[v].isnull().sum()

            # Convert missing values in a dataframe column to value
            df[v].fillna(replace_value, inplace=True)

            # Convert dataframe to best possible dtype
            df[v] = df[v].convert_dtypes()

            # Create log
            msg = f"Converted {number_of_missing_values_converted} missing values to {replace_value}."
            self.log[v]['convertBlankstoValue'] = msg

            if self.debug:
                print(f"For variable: {v}: {msg}")

        return df
    

    def compare_columns_A_B(self, df, A, B): 
        """
        A function to compare two columns A and B of a dataframe and 
        modify column A to B's value if A is greater than B
        
        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing the two columns
        A : str
            Name of the first column
        B : str
            Name of the second column
        
        Returns
        -------
        pandas.DataFrame
            Modified dataframe with column A equal to B if A was greater
        """

        def func(row):
            if pd.isnull(row[A]) or pd.isnull(row[B]):
                return (row[A])
            else:
                if row[A] > row[B]:
                    return row[B]
                else:
                    return row[A]

        self.init_log(A) # initialise log

        # Convert dataframe to best possible type
        df[[A,B]] = df[[A,B]].convert_dtypes()

        # Count the number of converted rows
        converted_rows = df.apply(lambda row: row[A] > row[B], axis = 1).sum()

        # Constraint A>=B without using for loop
        df[A] = df.apply(lambda x: func(x), axis = 1)

        # Convert dataframe to best possible type
        df[[A,B]] = df[[A,B]].convert_dtypes()

        # Create log
        msg = f"Converted {converted_rows} values in {A} to {B}."
        self.log[A]['compare_columns_A_B'] = msg

        if self.debug:
            print(f"For variable: {A}: {msg}")

        return df