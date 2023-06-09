from mz import utils_ as ut_
import pandas as pd
import numpy as np
import pprint
import os
from copy import deepcopy

class CleanData:
    """
    """

    def __init__(self,
        definitions=None,
        debug=True
    ):
        
        self.debug = debug

        # LOADING DEFAULTS
        self.folder_rawData = "rawData"
        self.folder_trainData = "trainData"

        self.output_type_data = 'csv'
        self.output_type_dict = 'xlsx'

        self.dict_var_varname = "NAME" # column in data dictionary containing variable names in input data
        self.dict_var_varcategory = "CATEGORY" # column in data dictionary setting the category of the variable name
        self.dict_var_type = "TYPE" # column in data dictionary setting the type of variable (string, numeric, date)
        self.dict_var_codings = "CODINGS" # column in data dictionary setting the codigns of variable (dataformat, categories)
        self.var_name_stripemptyspaces = False #If True, empty spaces will be stripped from variable names in input data, and from variables names listed in data dictionary.
        self.longitudinal_variableMarker = None #column header which contains the list of categories stipulating a list of longitudinal markers

        # LOADING DEFAULTS FOR DUPLICATED ROWS
        self.dropped_duplicated_rows_filename = "rowsRemoved.xlsx"
        self.suffix_dropped_duplicated_rows = "DD"

        # LOADING DEFAULTS FOR STANDARDISE TEXT
        self.suffix_standardise_text = "ST"
        self.options_standardise_text_case_type = "uppercase"
        self.options_standardise_text_exclude_list = []
        self.options_standardise_text_case_type_dict = {}

        # LOADING DEFAULTS FOR STANDARDISE DATES
        self.suffix_standardise_date = "DATE"
        self.options_standardise_date_format = "yyyy-mm-dd"
        self.options_faileddate_conversions_filename = 'failed_date_conversions.csv'

        # LOADING DEFAULTS FOR ASCII CONVERSION
        self.suffix_convert_ascii = "ASCII"
        self.options_convert_ascii_exclusion_list = []

        # LOADING DEFAULTS FOR CONSTRAINTS
        self.suffix_constraints = "CON"

        # LOAD DEFINITIONS
        self.definitions = definitions
        self._load_definitions()

        # LOAD INPUT DATA
        self.read_inputData(sheetname=self.definitions.RAWXLSX_SHEETNAME)

        # LOAD DATA DICTIONARY
        self.read_inputDict(sheetname=self.definitions.RAWDICTXLSX_SHEETNAME)

        # CHECK IF THE VARIABLES IN INPUT DATA MATCHES THE DATA DICTIONARY
        no_mismatch = self._check_variable_match_dict_data(strip_empty_spaces=self.var_name_stripemptyspaces)
        if not no_mismatch:
            print(f"Mismatched Variables:\n {self.var_diff_list}")

        # GET LIST OF LONGITUDINAL MARKERS.
        self._get_longitudinal_marker_list()

        # CREATE REQUIRED FOLDERS
        if not os.path.exists(self.train_data_path):
            os.makedirs(self.train_data_path)

        # GET CATEGORY: FIELD DICTIONARY
        self._get_field_category_from_dict()
        
        # GET TYPE: FIELD DICTIONARY
        self._get_dataType_from_dict()

        # SAVE NEW DATA AND DICTIONARY IN TRAINDATA PATH
        self._save_data_to_file()
        self._save_dict_to_file()

        
    def _update_defaults(self, var_to_update, new_value):
        if hasattr(self.definitions, new_value):
            attr = getattr(self.definitions, new_value)
            if attr is not None:
                setattr(self, var_to_update, attr)

    def _load_definitions(self):

        # Updating defaults
        self._update_defaults(var_to_update="folder_rawData", new_value="RAW_PATH")
        self._update_defaults(var_to_update="folder_trainData", new_value="TRAIN_PATH")
        self._update_defaults(var_to_update="dict_var_varname", new_value="DICT_VAR_VARNAME")
        self._update_defaults(var_to_update="dict_var_varcategory", new_value="DICT_VAR_VARCATEGORY")
        self._update_defaults(var_to_update="dict_var_type", new_value="DICT_VAR_TYPE")
        self._update_defaults(var_to_update="dict_var_codings", new_value="DICT_VAR_CODINGS")
        
        self._update_defaults(var_to_update="var_name_stripemptyspaces", new_value="VAR_NAME_STRIPEMPTYSPACES")
        
        # Updating defaults for OUTPUT TYPES
        self._update_defaults(var_to_update="output_type_data", new_value="OUTPUT_TYPE_DATA")
        self._update_defaults(var_to_update="output_type_dict", new_value="OUTPUT_TYPE_DICT")

        # Updating defaults for DROP DUPLICATES
        self._update_defaults(var_to_update="dropped_duplicated_rows_filename", new_value="OUTPUT_DROPPED_DUPLICATED_ROWS_FILENAME")
        self._update_defaults(var_to_update="suffix_dropped_duplicated_rows", new_value="SUFFIX_DROPPED_DUPLICATED_ROWS")

        # Updating defaults for STANDARDISE TEXT
        self._update_defaults(var_to_update="suffix_standardise_text", new_value="SUFFIX_STANDARDISE_TEXT")
        self._update_defaults(var_to_update="options_standardise_text_case_type", new_value="OPTIONS_STANDARDISE_TEXT_CASE_TYPE")
        self._update_defaults(var_to_update="options_standardise_text_exclude_list", new_value="OPTIONS_STANDARDISE_TEXT_EXCLUDE_LIST")
        self._update_defaults(var_to_update="options_standardise_text_case_type_dict", new_value="OPTIONS_STANDARDISE_TEXT_CASE_TYPE_DICT")

        # Updating defaults for STANDARDISE DATES
        self._update_defaults(var_to_update="suffix_standardise_date", new_value="SUFFIX_STANDARDISE_DATE")
        self._update_defaults(var_to_update="options_standardise_date_format", new_value="OPTIONS_STANDARDISE_DATE_FORMAT")
        self._update_defaults(var_to_update="options_faileddate_conversions_filename", new_value="OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME")

        # Updating defaults for CONVERTING ASCII
        self._update_defaults(var_to_update="suffix_convert_ascii", new_value="SUFFIX_CONVERT_ASCII")
        self._update_defaults(var_to_update="options_convert_ascii_exclusion_list", new_value="OPTIONS_CONVERT_ASCII_EXCLUSION_LIST")

        self._update_defaults(var_to_update="suffix_constraints", new_value="SUFFIX_CONSTRAINTS")


        self.prefix_path = self.definitions.PREFIX_PATH

        self.raw_data_path = self.prefix_path + self.folder_rawData + "\\"
        self.raw_data_filename = self.raw_data_path + self.definitions.RAWXLSX
        self.raw_data_dict_filename = self.raw_data_path + self.definitions.RAWDICTXLSX

        self.train_data_path = self.prefix_path + self.folder_trainData + "\\"

        # Initialise latest_filename for cleaned input data
        self.data_latest_filename = self.train_data_path + self.definitions.RAWXLSX
        self.data_latest_filename = ut_.change_extension(self.data_latest_filename, self.output_type_data)

        # Initialise latest filename for data dictionary
        self.dict_latest_filename = self.train_data_path + self.definitions.RAWDICTXLSX
        self.dict_latest_filename = ut_.change_extension(self.dict_latest_filename, self.output_type_dict)

        # Initialise settings for longitudinal data
        self._update_defaults(var_to_update="longitudinal_variableMarker", new_value="LONG_VAR_MARKER")

        self.longitudinal_marker_list = None #list of longitudinal markers

        
        self.raw_df = None #initialise raw data (dataframe)
        self.dict_df = None #initialise data dictionary (dataframe)
        self.clean_df = None #initialise cleaned data (dataframe)
        self.clean_dict_df = None #initialise cleaned data dictionary (dataframe)
        self.var_list = None #list of all variables (column headers) found in input data
        self.var_diff_list = None #list of discrepancies between data dictionary and input data
        self.cat_var_dict = None #dictionary with {cat: [list of variables]}
        self.type_var_dict = None #dictionary with {type: [list of variables]}

    def convert_2_dtypes(self, data):
        """Convert data (df) into best possible dtypes"""
        return data.convert_dtypes()

    def _get_longitudinal_marker_list(self):

        if self.longitudinal_variableMarker is not None:
            self.longitudinal_marker_list = list(self.raw_df[self.longitudinal_variableMarker].unique())
        else:
            self.longitudinal_marker_list = ["0"]
        
        if (self.debug):
            print(f"Extracting list of longitudinal markers: {self.longitudinal_marker_list}")
    
    def read_inputData(self, sheetname=None):
        """Reads raw data from input definitions and outputs it as a dataframe.
        Data can be in the following formats:
            a) Excel .xlsx
            b) Text .csv
        
        Parameters
        ----------
        sheetname : string, optional
            Name of the sheet in the excel file. If not specified, the first sheet will be read.
        
        Returns
        -------
        raw_df : pandas dataframe
            Dataframe containing the raw data.
        """

        if (self.debug):
            print(f"Reading raw data from filename: {self.raw_data_filename}")

        # Check if file exists
        if not ut_.check_filename(self.raw_data_filename):
            raise FileNotFoundError(f"File {self.raw_data_filename} cannot be found.")

        # Get filename extension
        extension = ut_.get_extension(self.raw_data_filename)
        if (self.debug):
            print(f"File extension: {extension}")
        
        # Get file_type
        try:
            if (extension=='xlsx'):
                file_type = 'excel'
                sheetnames = ut_.get_worksheet_names(self.raw_data_filename)
                if sheetname is None: # if sheetname is not given
                    sheetname = sheetnames[0] #read the first sheet

                    if (self.debug):
                        print(f"No sheetname given: sheetname assigned as {sheetname}.")
                else:
                    print(f"Sheetname is preassigned as {sheetname}.")
                self.raw_data_sheetname = sheetname
            elif (extension=='csv'):
                file_type = 'csv'
                        
        except ValueError as e:
            raise ValueError("Error in getting sheetname of file type xlsx: " + str(e)) from None

        try:
            if file_type=='excel':
                # Read file and output as dataframe
                self.raw_df = pd.read_excel(self.raw_data_filename,
                    sheet_name=sheetname
                )
            elif file_type=='csv':
                # Read file and output as dataframe
                self.raw_df = pd.read_csv(self.raw_data_filename)
        except ValueError as e:
            raise ValueError('Could not read sheet in excel file: ' + str(e)) from None
        
        if (self.debug):
            print(f"Input data loaded.")

        return self.raw_df

    def read_inputDict(self, sheetname=None):

        if (self.debug):
            print(f"Reading data dictionary from filename: {self.raw_data_dict_filename}")

        # Check if file exists
        if not ut_.check_filename(self.raw_data_dict_filename):
            raise FileNotFoundError(f"File {self.raw_data_dict_filename} cannot be found.")
        
        # Get filename extension
        extension = ut_.get_extension(self.raw_data_dict_filename)
        if (self.debug):
            print(f"File extension: {extension}")

        # Get file_type
        try:
            if (extension=='xlsx'):
                file_type = 'excel'
                sheetnames = ut_.get_worksheet_names(self.raw_data_dict_filename)
                if sheetname is None: # if sheetname is not given
                    sheetname = sheetnames[0] #read the first sheet

                    if (self.debug):
                        print(f"No sheetname given: sheetname assigned as {sheetname}.")
                else:
                    print(f"Sheetname is preassigned as {sheetname}.")
                self.raw_data_dict_sheetname = sheetname
                        
        except ValueError as e:
            raise ValueError("Error in getting sheetname of file type xlsx: " + str(e)) from None
        
        try:
            if file_type=='excel':
                # Read file and output as dataframe
                self.dict_df = pd.read_excel(self.raw_data_dict_filename,
                    sheet_name=sheetname
                )
        except ValueError as e:
            raise ValueError('Could not read sheet in excel file: ' + str(e)) from None
        
        if (self.debug):
            print(f"Data dictionary loaded.")

        return self.dict_df

    def _check_variable_match_dict_data(self, strip_empty_spaces=False):
        """Check if variables in dictionary match the field headers in self.raw_df. Problematic fields will be stored in self.var_diff_list."""

        # Load the variables names found in the data dictionary
        if self.dict_var_varname not in self.dict_df.columns:
            raise KeyError(f"Column {self.dict_var_varname} cannot be found in Data Dictionary. Please check that the the column exists in the Data Dictionary or specify the correct column name in the definitions.py file, under DICT_VAR_VARNAME.")

        # STRIP EMPTY SPACES
        if (strip_empty_spaces):
            self.clean_df = deepcopy(self.raw_df)
            self.clean_dict_df = deepcopy(self.dict_df)
            self.clean_df = ut_.strip_empty_spaces(self.clean_df)
            self.clean_dict_df = ut_.strip_empty_spaces(self.clean_dict_df)
            ut_.strip_string_spaces(self.clean_dict_df, col=self.dict_var_varname) #string spaces are not automatically stripped from data (prevent auto conversion to dates)
        else: 
            self.clean_df = deepcopy(self.raw_df)
            self.clean_dict_df = deepcopy(self.dict_df)

        # Load the column headers in self.clean_df
        var_clean_df_list = list(self.clean_df.columns)

        # Load the variables names found in the data dictionary
        var_dict_df_list = self.clean_dict_df[self.dict_var_varname].values.tolist()

        # Check if the variables in input data and dictionary matches
        self.var_diff_list = set(var_clean_df_list) ^ set(var_dict_df_list)

        # Save the list of variables if no discrepancies
        if (len(self.var_diff_list)==0):
            self.var_list = var_clean_df_list
            if (self.debug):
                print(f"No variable name mismatches found. Proceeding with next step of initialisation...")
        else:
            print("There is a mismatch in the variable names extracted from the input data and the data dictionary. Use cleanData.var_diff_list to extract list of mismatched variable names.")
        
        return len(self.var_diff_list)==0


    def _save_data_to_file(self):

        file_ext = ut_.get_extension(self.data_latest_filename)

        if (file_ext=='csv'):
            ut_.save_df_as_csv(self.clean_df, self.data_latest_filename, index=False)

        elif (file_ext=='xlsx'):
            ut_.save_df_as_excel(self.clean_df, 
                excel_file_name = self.data_latest_filename, 
                sheet_name = self.raw_data_sheetname,
                index = False # not saving the index
            )

        else:
            raise ValueError(f"Not able to save data to file for extension type: {file_ext}")

    def _save_dict_to_file(self):

        file_ext = ut_.get_extension(self.dict_latest_filename)

        if (file_ext=='csv'):
            ut_.save_df_as_csv(self.clean_dict_df, self.dict_latest_filename, index=False)
        
        elif (file_ext=='xlsx'):
            ut_.save_df_as_excel(self.clean_dict_df,
                excel_file_name = self.dict_latest_filename,
                sheet_name = self.raw_data_dict_sheetname,
                index = False # not saving the index
            )

        else:
            raise ValueError(f"Not able to save dictionary to file for extension type: {file_ext}")
        
    def update_data(self, new_df, filename_suffix=""):
        """Update and replace the input data in the CleanData class with new input data"""

        if (self.debug):
            print(f"Replacing the input data...")
        
        try:
            # Get new filename
            old_filename = deepcopy(self.data_latest_filename)
            self.data_latest_filename = ut_.update_filename_with_suffix(filename=self.data_latest_filename, suffix=filename_suffix)

            # Update latest clean df to output_df
            old_df = deepcopy(self.clean_df)
            self.clean_df = deepcopy(new_df)
            self.clean_df.reset_index(drop=True, inplace=True) #reset the index

            self._save_data_to_file()

            print(f"Replacing the input data complete. new filename: {self.data_latest_filename}")
        except:
            self.data_latest_filename = deepcopy(old_filename) # return
            self.clean_df = deepcopy(old_df) # return

            raise ValueError(f"Not able to save data to file.")

        
    def _get_field_category_from_dict(self):

        # Extract dataframe columns with variable name and variable category
        A = self.dict_var_varname
        B = self.dict_var_varcategory
        cat_df = self.clean_dict_df[[A, B]]

        # Create a dictionary
        self.cat_var_dict = {key: list(cat_df[A][cat_df[B] == key]) for key in cat_df[B].unique()}

    def _get_dataType_from_dict(self):

        # Extract dataframe columns with variable name and variable category
        A = self.dict_var_varname
        B = self.dict_var_type
        cat_df = self.clean_dict_df[[A, B]]

        # Create a dictionary
        self.type_var_dict = {key: list(cat_df[A][cat_df[B] == key]) for key in cat_df[B].unique()}



    # DROP DUPLICATES
    def drop_duplicate_rows(self):
        """Use to drop duplicate rows from the input dataframe. Performs the following steps:
        1) Exclude variables of the "Index" category from the duplicate search
        2) Make a working copy of the input dataframe
        3) Get the index of duplicate rows
        4) Drop the duplicate rows from the dataframe
        5) Get the dropped rows from the original dataframe and save them as an excel file
        6) Update the new filename and the new input dataframe        
        """

        if (self.debug):
            print(f"Dropping duplicate rows in input data...")

        # Exclude variables of the "Index"  category from the duplicate search
        subset_list = ut_.remove_items(self.cat_var_dict["Index"], self.var_list)

        # Get a working copy of latest data dataframe
        df = deepcopy(self.clean_df)

        # Get index of duplicate rows
        duplicated_index = df.duplicated(keep='first', subset=subset_list)

        # Drop duplicate rows
        output_df = df.drop_duplicates(subset=subset_list, keep='first', inplace=False)

        # Get the dropped rows from original dataframe
        dropped_rows_df = df.loc[duplicated_index]
        no_dropped_rows = dropped_rows_df.shape[0]
        
        if (self.debug):
            print(f"No. of dropped rows: {no_dropped_rows}")

        # Save dropped rows as excel file
        ut_.save_df_as_excel(dropped_rows_df,
            excel_file_name = self.train_data_path + self.dropped_duplicated_rows_filename,
            sheet_name = "Sheet1",
            index = True
        )

        # Update new filename and new input data
        self.update_data(new_df=output_df, filename_suffix=self.suffix_dropped_duplicated_rows)

    # STANDARDISE TEXT
    def standardise_text_case_conversion(self, data, case_type):
        if case_type == 'uppercase':
            data = data.astype(str).str.upper()
        elif case_type == 'lowercase':
            data = data.astype(str).str.lower()
        elif case_type == 'capitalise':
            data = data.astype(str).str.title()

        return data

    def standardise_text(self):
        """"""

        if (self.debug):
            print(f"Standardising text in input data...")

        # Load case_type
        def_case_type = self.options_standardise_text_case_type #set default case_type
        exclude_list = self.options_standardise_text_exclude_list
        case_type_dict = self.options_standardise_text_case_type_dict

        # ExTRACT variables of the "Index"  category
        subset_list = self.cat_var_dict["Index"]

        # Get a working copy of latest data dataframe
        df = deepcopy(self.clean_df)

        # convert data_df to best possible dtypes
        output_df = self.convert_2_dtypes(df)

        # Loop through df and convert all strings to specified case
        for col in output_df.columns:
            if col not in subset_list: # exclude variables marked as index type
                if col not in exclude_list: # exclude varaibles in exclude_list

                    # Overwrite default case_type with specified type in dict
                    case_type = def_case_type
                    if col in case_type_dict:
                        case_type = case_type_dict[col]
                    
                    # Perform conversion
                    if output_df[col].dtype == 'object':
                        output_df[col] = self.standardise_text_case_conversion(output_df[col], case_type)
                    elif output_df[col].dtype == 'string':
                        output_df[col] = self.standardise_text_case_conversion(output_df[col], case_type)
        
        # Update new filename and new input data
        self.update_data(new_df=output_df, filename_suffix=self.suffix_standardise_text)

    # CONVERTING ASCII
    def converting_ascii(self, ascii_exclusion_list=None):
        """Converts all characters in input data to ASCII-compatible format

        Parameters
        ----------
        ascii_exclusion_list : list, default = self.options_convert_ascii_exclusion_list
            List of characters to not replace

        Returns
        -------
        self : object
            Returns self with clean_df updated with the ascii compatible data

        """

        # Load options
        ascii_exclusion_list = ascii_exclusion_list or self.options_convert_ascii_exclusion_list

        if (self.debug):
            print(f"Converting all characters to ASCII-compatible in input data...")
            print(f"List of Exclusions: \n{ascii_exclusion_list}")

        # Get a working copy of latest data dataframe
        df = deepcopy(self.clean_df)

        # convert data_df to best possible dtypes
        output_df = self.convert_2_dtypes(df)

        # replace all characters in list of exclusions
        list_of_cols_with_ex_char = []
        for col in output_df.columns:
            if output_df[col].dtype == object or output_df[col].dtype == "string":
                for ex_char in ascii_exclusion_list:
                    if any(ex_char in s for s in output_df[col]):
                        replace_str = f"-~*{ex_char}*~-"
                        output_df[col] = output_df[col].str.replace(ex_char, replace_str, regex=False)
                        list_of_cols_with_ex_char.append(col)

        # convert all string/object columns to ascii-compatible characters
        output_df = ut_.convert_to_ascii(output_df)

        # revert all characters in list of exclusions
        for col in list_of_cols_with_ex_char:
            for ex_char in ascii_exclusion_list:
                replace_str = f"-~*{ex_char}*~-"
                replace_str = ut_.convert_to_ascii(replace_str)
                output_df[col] = output_df[col].str.replace(replace_str, ex_char, regex=False)


        # Update new filename and new input data
        self.update_data(new_df=output_df, filename_suffix=self.suffix_convert_ascii)

    
    # STANDARDISE DATES
    def standardise_date(self, def_date_format=None, faileddate_conversions_filename=None):
        """Standardises the date/time in input data.

        Standardise the date format of variables of the TYPE "date" (as specified in the data dictionary). Primarily changes the format of the column as per the predefined standard date and time format, as specified in OPTIONS_STANDARDISE_DATE_FORMAT (global definitions).

        It also stores the failed conversions in a csv file, as specified in OPTIONS_FAILEDDATE_CONVERSIONS_FILENAME (global definitions)
        
        Parameters
        ----------
        def_date_format : string, optional
            the standard date format to use for all dates (ignore if already specified in global definitions, default is 'yyyy-mm-dd') [follows format used in ms-excel, see ref. https://www.ablebits.com/office-addins-blog/change-date-format-excel/]

        faileddate_conversions_filename : string, optional
            the filename.csv for storing list of failed date conversions (ignore if already specified in global definitions, default is 'failed_date_conversions.csv') [only csv allowed]
        
        Returns
        -------
        No value returned, updates the dataFile given.
        """

        if (self.debug):
            print(f"Standardising date/time in input data...")

        # ExTRACT variables of the "Index"  category
        if 'Index' in self.cat_var_dict:
            index_list = self.cat_var_dict["Index"]
            chosen_index = index_list[0]
        else: 
            chosen_index = None

        # Load standardised date format
        def_date_format = def_date_format or self.options_standardise_date_format
        def_date_format_convert = ut_.mapping_dictDateFormatConversion(def_date_format)

        # Get list of variables defined as 'date' in TYPE
        dateVar_list = self.type_var_dict['date']

        # Get a working copy of latest data dataframe
        df = deepcopy(self.clean_df)

        # convert data_df to best possible dtypes
        output_df = self.convert_2_dtypes(df)

        # initialise empty dataframe to store failed conversions
        failedIndices_df = pd.DataFrame()
        faileddate_conversions_filename = faileddate_conversions_filename or self.options_faileddate_conversions_filename

        #
        for dateVar in dateVar_list:
            
            dateColFieldFormat = deepcopy(def_date_format_convert) # the date format to convert to

            # the date format to convert from
            raw_dateColFieldFormat = self.clean_dict_df[self.clean_dict_df[self.dict_var_varname]==dateVar][self.dict_var_codings].values[0]
            raw_dateColFieldFormat = ut_.mapping_dictDateFormatConversion(str(raw_dateColFieldFormat))
            
            # Conversion (Easiest Case [Excel])
            if output_df[dateVar].dtype == 'datetime64[ns]': # when raw excel column is specified as datatype: date in excel
                output_df[dateVar] = pd.to_datetime(output_df[dateVar], errors="ignore").dt.strftime(dateColFieldFormat)

            elif output_df[dateVar].dtype == 'string': # when column is specified as string

                # Check if date format is usable. If not, learn one from the data
                if raw_dateColFieldFormat == '' or raw_dateColFieldFormat=='nan':
                    if (self.debug):
                        print(f'Standardise date: raw_dateCOlFieldFormat for variable {dateVar} is not valid.')

                    raw_dateColFieldFormat = ut_.date_format_search(output_df[dateVar])
                    if (self.debug):
                        print(f"Using {raw_dateColFieldFormat} as date format.")

                # Conversion
                output_df = ut_.strip_string_spaces(output_df, col=dateVar)
                output_df[dateVar] = pd.to_datetime(output_df[dateVar], format=raw_dateColFieldFormat, errors="coerce").dt.strftime(dateColFieldFormat)

            # save failed conversions to dataframe
            if chosen_index is not None:
                failedIndices_df[dateVar] = output_df[output_df[dateVar].isna()][chosen_index]
            else: # if chosen_index is not available, use df index
                failedIndices_df[dateVar] = output_df[output_df[dateVar].isna()].index

            if (self.output_type_data == 'csv'): #workaround to prevent automatic date conversion of csv by ms-excel
                output_df[dateVar] = ' ' + output_df[dateVar].astype(str) 

            # update dict 'CODINGS' column with new standardised date format
            self.clean_dict_df.loc[self.clean_dict_df[self.dict_var_varname]==dateVar, self.dict_var_codings] = def_date_format

        # Update new filename and new input data
        self.update_data(new_df=output_df, filename_suffix=self.suffix_standardise_date)

        # Update new data dictionary with new standardised date format
        self._save_dict_to_file()

        

        # Save failed conversions to file
        f_filename = self.train_data_path + faileddate_conversions_filename
        ut_.save_df_as_csv(failedIndices_df, f_filename, index=True)