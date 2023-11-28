from bdarpack import utils_ as ut_
import pandas as pd
from copy import deepcopy
import os, sys
import pickle
from bdarpack.Transformer import Transformer
from bdarpack.GaussianCopula import GaussianCopula
from bdarpack.PrivacyMetric import PrivacyMetric as PM
from pprint import pprint

def load_TC(defi):
    """Function to load saved TC instance from definitions."""

    # Get filename of spreadsheet of filenames
    t = defi.TRAINXLSX.split('.')[0]
    dir_path = os.path.dirname(sys.argv[0])
    CLOF_filename = f"{dir_path}/{defi.SYN_PATH}/{t}-{defi.OUTPUT_GENERAL_PREFIX}-CL-OF.{defi.OUTPUT_TYPE_DATA}"

    # read file
    if (defi.OUTPUT_TYPE_DATA=='csv'):
        CLOF_df = pd.read_csv(CLOF_filename)
    elif (defi.OUTPUT_TYPE_DATA=='xlsx'):
        CLOF_df = pd.read_excel(CLOF_filename, sheet_name="SHEET1")

    # Get filename of pickle
    tc_inst_filename = CLOF_df.loc[CLOF_df['Type'] == 'tc-class-instance', 'Object'].item()

    # Load pickle
    with open(tc_inst_filename, 'rb') as fl:
        tc = pickle.load(fl)
    
    return tc

class TabulaCopula:
    """
    Wrapper for performing copula/conditional-copula (Gaussian) for Tabular-type data.

    Inputs:

        conditionalSettings_dict (dict): dictionary of inputs for using conditional-copula

        output_general_prefix (str): Prefix used for all output files, e.g. "EXPT_1". If not None, replaces settings in definitions. Default is None.

        metaData_transformer (dict): dictionary of inputs for the Transformer class initialisation (ref Transformer metaData(dict))
    
        var_list_filter (list): List of variables to transform. Default is None (all will be transformed)

        removeNull (bool): Whether to remove all null values prior to transformation. Default is False.
        
        sampling (float): Percentage of sample points draw from the transformed dataframe, leaving the rest as control. Default is 1 (use all). Note that the sampling is done after the transformation, not before.

        debug (bool): Flag to print debugging lines. Default is `True`.

    Example inputs:
        conditionalSettings_dict = {
            "set_1": {
                "bool": True,
                "parent_conditions": { # 2 parents, the `Y` in `P(X | Y)`.
                    "SurveyYr": { # split variable into 2 sets
                        "condition": "set",
                        "condition_value": {
                            1: ["2009_10"],
                            2: ["2011_12"]
                        }
                    },
                    "Age": { # split variable into 3 sets based on range
                        "condition": "range",
                        "condition_value": {
                            1: [">=3", "<79"],
                            2: ["<3"],
                            3: [">=79"]
                        }
                    }
                },
                "conditions_var": ["Age"], # the `Y` to keep constant while generating values of `X` in `P(X | Y)`. Can be a float, in which case it is a threshold to fix all variables with pairwise correlation (with X) above then said threshold.
                "children": ['AgeMonths'] #variable for which to learn the joint conditional distributions on, the `X` in `P(X | Y)`. Can be a string: "allOthers".
            }
        }

    Change log:
        (MZ) 07-09-2023: add sampling option to transformed data (form disjoint subsets for training and control).
        (MZ) 21-09-2023: add functionality to save class as pickle, save output filenames dictionary to csv.
        (MZ) 25-09-2023: add option indexTrue to function _save_data_to_file
        (MZ) 25-09-2023: update save_outputFilenames to save dataframe index columsn
        (MZ) 25-09-2023: fix bug which overwrites dictionary definition of output_general_prefix with ''
        (MZ) 29-09-2023: add privacy leakage functionalities
    """

    def __init__(self,
        definitions=None,
        output_general_prefix=None,
        conditionalSettings_dict=None,
        metaData_transformer=None,
        var_list_filter=None,
        removeNull=False,
        sampling = None,
        debug=True
    ):
        
        self.debug = debug

        # LOADING DEFAULTS
        self.folder_trainData = "trainData"
        self.folder_synData = "synData"
        self.folder_privacyMetrics = "privacyMetrics"

        self.output_general_prefix = ''
        self.sampling = 1
        self.privacy_batch_n = 3

        self.output_type_data = 'csv'
        self.output_type_dict = 'xlsx'
        self.output_type_obj = 'pkl'

        self.dict_var_varname = "NAME" # column in data dictionary containing variable names in input data
        self.dict_var_varcategory = "CATEGORY" # column in data dictionary setting the category of the variable name
        self.dict_var_vartype = "TYPE" # column in data dictionary containing variable types in input data

        self.conditional_set_bool = False # flag set to true when filenames initialised for conditional setup

        # LOAD DEFINITIONS
        # self.definitions = definitions # deprecated to allow saving of instance as pickle
        self._load_definitions(definitions)

        # REPLACE DEFINTIONS WITH USER-INPUTS (FUNCTION LEVEL)
        self.output_general_prefix = output_general_prefix if output_general_prefix is not None else self.output_general_prefix 
        self.metaData_transformer = metaData_transformer
        self.var_list_filter = var_list_filter # list of variables to transform (subset of all input variables)
        self.removeNull = removeNull

        if sampling is not None:
            self.sampling = sampling if sampling > 0.01 and sampling <= 1 else 1 # float to decide proportion of transformed samples to use (forced to 1 if invalid)

        self.conditionalSettings_dict = conditionalSettings_dict

        # LOAD DATA DICTIONARY
        self.read_inputDict(sheetname=definitions.TRAINDICTXLSX_SHEETNAME)

        # LOAD INPUT DATA
        self.read_inputData(sheetname=definitions.TRAINXLSX_SHEETNAME)

        # CREATE REQUIRED FOLDERS
        if not os.path.exists(self.syn_data_path):
            os.makedirs(self.syn_data_path)

        if not os.path.exists(self.privacyMetrics_path):
            os.makedirs(self.privacyMetrics_path)

        # CREATE OUTPUT FILENAMES AND STORAGE LOCATIONS
        self.build_filenames()
        self.build_storage()

    def _update_defaults(self, var_to_update, new_value, definitions):
        if hasattr(definitions, new_value):
            attr = getattr(definitions, new_value)
            if attr is not None:
                setattr(self, var_to_update, attr)

    def _load_definitions(self, definitions):

        # Updating defaults
        self._update_defaults(var_to_update="folder_trainData", new_value="TRAIN_PATH", definitions=definitions)
        self._update_defaults(var_to_update="folder_synData", new_value="SYN_PATH", definitions=definitions)
        self._update_defaults(var_to_update="folder_privacyMetrics", new_value="PRIV_PATH", definitions=definitions)

        self._update_defaults(var_to_update="dict_var_varname", new_value="DICT_VAR_VARNAME", definitions=definitions)
        self._update_defaults(var_to_update="dict_var_varcategory", new_value="DICT_VAR_VARCATEGORY", definitions=definitions)
        self._update_defaults(var_to_update="dict_var_type", new_value="DICT_VAR_TYPE", definitions=definitions)
        
        # Updating defaults for OUTPUT TYPES
        self._update_defaults(var_to_update="output_general_prefix", new_value="OUTPUT_GENERAL_PREFIX", definitions=definitions)
        self._update_defaults(var_to_update="output_type_data", new_value="OUTPUT_TYPE_DATA", definitions=definitions)
        self._update_defaults(var_to_update="output_type_dict", new_value="OUTPUT_TYPE_DICT", definitions=definitions)

        # Update defaults for privacy leakage testing
        self._update_defaults(var_to_update="sampling", new_value="SAMPLING", definitions=definitions)
        self._update_defaults(var_to_update="privacy_batch_n", new_value="PRIVACY_BATCH_N", definitions=definitions)

        self.prefix_path = definitions.PREFIX_PATH

        self.trainxlsx = definitions.TRAINXLSX
        self.traindictxlsx = definitions.TRAINDICTXLSX

        self.train_data_path = self.prefix_path + self.folder_trainData + "\\"
        self.train_data_filename = self.train_data_path + definitions.TRAINXLSX
        self.train_data_dict_filename = self.train_data_path + definitions.TRAINDICTXLSX

        self.syn_data_path = self.prefix_path + self.folder_synData + "\\"
        self.privacyMetrics_path = self.prefix_path + self.folder_privacyMetrics + "\\"


        self.train_df = None #initialise training data (dataframe)
        self.dict_df = None #initialise data dictionary (dataframe)
        self.var_list = None #list of all variables (column headers) found in input data
        self.processed_var_list = None #list of all variables (column headers) that have been transformed
        self.transformed_df = None #initialise transformed training data (dataframe) / replaced with transformed data after sampling (disjoint with self.control_df)
        self.control_df = None # the dataframe that is not sampled for training (left as control for privacy leakage testing)
        self.curated_train_df = None #initialise curated data prior to transformation (dataframe)
        self.syn_samples_df = None #initialise synthetic samples (dataframe)
        self.syn_samples_conditional_df = None #initialise conditional synthetic samples (dataframe)
        self.reversed_df = None #initialise reversed synthetic samples (dataframe)
        self.reversed_conditional_df = None #initialise conditional reversed synthetic samples (dataframe)
        self.reversed_control_df = None #initialise reversed control_df (dataframe)
        self.reversed_transformed_df = None #initialise reversed transformed_df (dataframe)

        self.privacyMetricEval = None #initialise privacy metric evaluator
        self.privacyMetricEval_cond = None #initialise privacy metric evaluator for conditional copula
        self.privacyMetricResults = {} #initialise privacy metric results dictionary

    
    def read_inputData(self, sheetname=None):
        """Reads training data from input definitions and outputs it as a dataframe.
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
            print(f"Reading training data from filename: {self.train_data_filename}")

        # Check if file exists
        if not ut_.check_filename(self.train_data_filename):
            raise FileNotFoundError(f"File {self.train_data_filename} cannot be found.")
        
        # Get filename extension
        extension = ut_.get_extension(self.train_data_filename)
        if (self.debug):
            print(f"File extension: {extension}")

        # Get file_type
        try:
            if (extension=='xlsx'):
                file_type = 'excel'
                sheetnames = ut_.get_worksheet_names(self.train_data_filename)
                if sheetname is None: # if sheetname is not given
                    sheetname = sheetnames[0] #read the first sheet

                    if (self.debug):
                        print(f"No sheetname given: sheetname assigned as {sheetname}.")
                else:
                    print(f"Sheetname is preassigned as {sheetname}.")
                self.train_data_sheetname = sheetname
            elif (extension=="csv"):
                file_type = 'csv'
                        
        except ValueError as e:
            raise ValueError("Error in getting sheetname of file type xlsx: " + str(e)) from None

        try:
            if file_type=='excel':
                # Read file and output as dataframe
                self.train_df = pd.read_excel(self.train_data_filename,
                    sheet_name=sheetname
                )
            elif file_type=="csv":
                # Read file and output as dataframe
                self.train_df = pd.read_csv(self.train_data_filename)

        except ValueError as e:
            raise ValueError('Could not read sheet in excel file: ' + str(e)) from None
        
        # Convert columns to "string" type based on data dictionary settings
        var_names = [row[self.dict_var_varname] for index, row in self.dict_df.iterrows() if row[self.dict_var_vartype] == 'string']
        self.train_df[var_names] = self.train_df[var_names].astype("str")


        if (self.debug):
            print(f"Input data loaded.")

        # Initialise list of variables found in input dataset
        self.var_list = list(self.train_df.columns)

        if (self.debug):
            print(f"Total number of variables in input data: {len(self.var_list)}")

        return self.train_df

    def read_inputDict(self, sheetname=None):

        if (self.debug):
            print(f"Reading data dictionary from filename: {self.train_data_dict_filename}")

        # Check if file exists
        if not ut_.check_filename(self.train_data_dict_filename):
            raise FileNotFoundError(f"File {self.train_data_dict_filename} cannot be found.")
        
        # Get filename extension
        extension = ut_.get_extension(self.train_data_dict_filename)
        if (self.debug):
            print(f"File extension: {extension}")

        # Get file_type
        try:
            if (extension=='xlsx'):
                file_type = 'excel'
                sheetnames = ut_.get_worksheet_names(self.train_data_dict_filename)
                if sheetname is None: # if sheetname is not given
                    sheetname = sheetnames[0] #read the first sheet

                    if (self.debug):
                        print(f"No sheetname given: sheetname assigned as {sheetname}.")
                else:
                    print(f"Sheetname is preassigned as {sheetname}.")
                self.train_data_dict_sheetname = sheetname
                        
        except ValueError as e:
            raise ValueError("Error in getting sheetname of file type xlsx: " + str(e)) from None
        
        try:
            if file_type=='excel':
                # Read file and output as dataframe
                self.dict_df = pd.read_excel(self.train_data_dict_filename,
                    sheet_name=sheetname
                )
        except ValueError as e:
            raise ValueError('Could not read sheet in excel file: ' + str(e)) from None
        
        if (self.debug):
            print(f"Data dictionary loaded.")

        return self.dict_df

    def transform(self, metaData=None, var_list=None):
        """
        Change log:
            -MZ 07-09-2023: add sampling option to transformed data (form disjoint subsets for training and control)
        """

        if metaData is None:
            metaData = deepcopy(self.metaData_transformer)

        if var_list is None:
            var_list = deepcopy(self.var_list_filter)

        # Initialise Transformer using given metaData
        transformer = Transformer(
            metaData = metaData,
            var_list = var_list,
            removeNull = self.removeNull,
            debug = self.debug
        )
        self.transformed_df = transformer.transform(self.train_df)

        # Sampling subset of transformed data for training, leaving the rest for control (7 Sept 2023-MZ)
        if self.sampling != 1:
            self.transformed_df, self.control_df = ut_.df_sampling(self.transformed_df, p=self.sampling)
        else:
            self.control_df = None

        self.processed_var_list = list(transformer.transformer_meta_dict.keys())
        self.curated_train_df = transformer.data_curated_df

        # Save Transformer (main)
        self.storage['transformer'] = transformer

        # Save transformed data (output to file)
        self._save_data_to_file(self.transformed_df, self.output_filenames['transformed'])
        self._save_data_to_file(self.curated_train_df, self.output_filenames['curated'])
        if self.control_df is not None:
            self._save_data_to_file(self.control_df, self.output_filenames["control"])

        return self.transformed_df
    
    def transform_conditional(self, metaData=None):
        # Change Log: 05-07-2023

        trainData = self.train_df # initialise data to be transformed
        transformedData = self.transformed_df # initialise transformed dataframe (FULL)

        if metaData is None: #not used anymore
            metaData = deepcopy(self.metaData_transformer)
        
        for set_no, conditionalBody in self.conditionalSettings_dict.items():

            if (conditionalBody["bool"]):
                    
                # Build Conditional Set-Index (build permutations)
                full_list_set_index = self.set_index_permutations_dict[set_no]

                # Get List of Parents
                parentVar_list = list(conditionalBody["parent_conditions"].keys())

                # Build Condition Array to Filter Out Irrelevant Rows
                cond_array = dict() #initialise condition array
                
                for merged_set_index in full_list_set_index: # e.g. "1-1-1", "1-2-1"
                    
                    cond_array[merged_set_index] = None # initialise condition array dict for each permutation
                    grp_set_index = str(merged_set_index).split("-")

                    for set_index, parentVar in zip(grp_set_index, parentVar_list):

                        parentVarBody = conditionalBody["parent_conditions"][parentVar] # get corresponding parent body
                        set_values = parentVarBody["condition_value"][int(set_index)] # get corresponding value from parent body
                        sub_cond_array = None

                        for set_value in set_values: # build sub-condition array by looping through all values in condition_value[set_index]

                            if (parentVarBody['condition']=="set"):

                                t_trainData_pVar = trainData[parentVar].astype('object').apply(str) # parent data column

                                if (sub_cond_array is None): # first entry
                                    sub_cond_array = (t_trainData_pVar.str.upper() == str(set_value).upper())
                                else: # subsequent entries
                                    sub_cond_array = sub_cond_array | (t_trainData_pVar.str.upper() == str(set_value).upper())

                            elif (parentVarBody['condition']=="range"):

                                t_trainData_pVar = trainData[parentVar].astype('float')  # parent data column

                                if (sub_cond_array is None): # first entry
                                    sub_cond_array = eval("t_trainData_pVar" + set_value)
                                else: # subsequent entries
                                    sub_cond_array = sub_cond_array & eval("t_trainData_pVar" + set_value)

                        # Add derived sub_cond_array into cond_array, corresponding to current merged_set_index permutation
                        if cond_array[merged_set_index] is None:
                            cond_array[merged_set_index] = sub_cond_array
                        else: # collect all the sub_cond_array(s) using the AND operation
                            cond_array[merged_set_index] = cond_array[merged_set_index] & sub_cond_array

                        
                # Define Conditional-Transformer as Full Transformer (save transformer)
                self.storage['cond_transformer'][set_no] = self.storage['transformer']

                # Filter Out Irrelevant Rows using Condition Array, then SAVE
                for merged_set_index, set_cond in cond_array.items():

                    transformed_filtered = transformedData[set_cond].copy()

                    # If null settings is 'mean'/'median'/'mode', update new mean/median/mode for null values
                    # (1) filter for all relevant children variables
                    if (conditionalBody["children"] == "allOthers"):
                        # childVarList = list(metaData.keys()) #replace with self.processed_var_list
                        childVarList = deepcopy(self.processed_var_list)
                        childVarList = [elem for elem in childVarList if elem not in parentVar_list]
                    else:
                        childVarList = conditionalBody['children']

                    # (2) update with new null values
                    transformed_filtered = self._conditional_update_newNullValue(childVarList, transformed_filtered)

                    # Save filtered transformed_data (output to file)
                    self._save_data_to_file(transformed_filtered, self.output_filenames['conditional_transformed'][set_no][merged_set_index])

        return 0

    
    def reverse_transform(self, transformed_df=None, conditional_transformed_df=None, control_transformed_df=None):
        """
        Change log:
            -MZ 07-09-2023: add reverse operation on control data
        """

        # Get data to reverse
        if transformed_df is not None:
            df = transformed_df
        else:
            df = self.syn_samples_df

        if conditional_transformed_df is not None:
            cond_df = conditional_transformed_df
        else: 
            cond_df = self.syn_samples_conditional_df

        if control_transformed_df is not None:
            control_df = control_transformed_df
        else:
            control_df = self.control_df

        # Get saved transformer from storage
        transformer = self.storage['transformer']

        # Reverse the transformation
        if df is not None:
            self.reversed_df = transformer.reverse(df)

        # Reverse the conditional transformation
        if cond_df is not None:
            self.reversed_conditional_df = transformer.reverse(cond_df)

        # Reverse the control data transformation
        if control_df is not None:
            self.reversed_control_df = transformer.reverse(control_df)
            self.reversed_transformed_df = transformer.reverse(self.transformed_df)

        # Output to file
        self._save_data_to_file(self.reversed_df, self.output_filenames["reversed_samples"])
        if cond_df is not None:
            self._save_data_to_file(self.reversed_conditional_df, self.output_filenames["conditional_reversed_samples"])

        if control_df is not None:
            self._save_data_to_file(self.reversed_control_df, self.output_filenames["controlReversed_samples"])
            self._save_data_to_file(self.reversed_transformed_df, self.output_filenames["training_samples"])

        return self.reversed_df, self.reversed_conditional_df
    
    def print_details_copula(self):

        # Get Copula
        cp = self.storage['copula']
        cp.print_copula_params()

        # Get Conditional Copula
        if self.conditional_set_bool:
            for set_no, conditionalBody in self.conditionalSettings_dict.items():
                if set_no in self.storage['cond_copula']:
                    for merged_set_index, b in self.storage['cond_copula'][set_no].items():

                        pprint(f'Printing Conditional-Copula Parameters for {set_no}: {merged_set_index}')

                        cp_cond = self.storage['cond_copula'][set_no][merged_set_index]
                        cp_cond.print_copula_params()
        
        return 0
    
    def fit_gaussian_copula(self, correlation_method='kendall', marginal_dist_dict=None):

        # Get transformed data
        transformed_df = self.transformed_df

        # Fit Gaussian Copula using given options
        gaussian_copula = GaussianCopula(debug=self.debug, correlation_method=correlation_method)
        gaussian_copula.fit(transformed_df, marginal_dist_dict=marginal_dist_dict)

        # Save learned Gaussian Copula
        self.storage['copula'] = gaussian_copula

    def fit_gaussian_copula_conditional(self, correlation_method='kendall', marginal_dist_dict=None):
        """Build Conditional Copula for given conditional_dict"""

        for set_no, conditionalBody in self.conditionalSettings_dict.items():

            if (conditionalBody["bool"]):

                # pprint(set_no)
                # pprint(conditionalBody)

                # Build Conditional Set-Index (build permutations)
                full_list_set_index = self.set_index_permutations_dict[set_no]

                # Initialise storage for set_no
                self.storage['cond_copula'][set_no] = {}

                for merged_set_index in full_list_set_index: # e.g. "1-1-1", "1-2-1"

                    # Read Transformed-Conditional Dataset from Stored CSVs
                    transformed_filtered_conditional_filename = self.output_filenames['conditional_transformed'][set_no][merged_set_index]
                    transformed_filtered_conditional = pd.read_csv(transformed_filtered_conditional_filename)

                    if (self.debug):
                        print(transformed_filtered_conditional)

                    # Fit Gaussian Copula using given options
                    gaussian_copula_conditional = GaussianCopula(debug=self.debug, correlation_method=correlation_method)
                    gaussian_copula_conditional.fit(transformed_filtered_conditional, marginal_dist_dict=marginal_dist_dict)

                    if ( not gaussian_copula_conditional.fitted):
                        print(f"Building conditional-copulae for {set_no}-{merged_set_index} Failed!")

                    # Save learned Gaussian Copula
                    self.storage['cond_copula'][set_no][merged_set_index] = gaussian_copula_conditional


    def sample_gaussian_copula(self, sample_size=1, conditions=None):

        # Get Copula 
        gaussian_copula = self.storage['copula']

        # Sample from Copula
        syn_samples_df = gaussian_copula.sample(size=sample_size, conditions=conditions)

        # Save generated samples
        self.syn_samples_df = syn_samples_df

        # Output to file
        self._save_data_to_file(self.syn_samples_df, self.output_filenames['synthetic_samples'])

    def sample_gaussian_copula_conditional(self):

        samples = deepcopy(self.syn_samples_df) # Get generated set of synthetic samples

        for set_no, conditionalBody in self.conditionalSettings_dict.items():

            if (conditionalBody["bool"]):

                # Get Corresponding Transformer
                cond_transformer = self.storage['cond_transformer'][set_no]
                if (self.debug):
                    pprint(cond_transformer.transformer_meta_dict)

                # Build Conditional Set-Index (build permutations)
                full_list_set_index = self.set_index_permutations_dict[set_no]

                # Get List of Parents
                parentVar_list = list(conditionalBody["parent_conditions"].keys())

                # Filter for all relevant children variables
                if (conditionalBody["children"] == "allOthers"):
                    childVarList = deepcopy(self.processed_var_list)
                    childVarList = [elem for elem in childVarList if elem not in parentVar_list]
                else:
                    childVarList = conditionalBody['children']

                # Build list of transformed child variable names
                childVarTransform_meta_outputfields = []
                for childVar in childVarList:
                    a = cond_transformer.transformer_meta_dict[childVar]['output_fields'].keys()
                    childVarTransform_meta_outputfields = childVarTransform_meta_outputfields + list(a)


                # Build Condition Array to Filter Out Irrelevant Rows
                cond_array = dict() #initialise condition array

                for merged_set_index in full_list_set_index: # e.g. "1-1-1", "1-2-1"
                    
                    cond_array[merged_set_index] = None # initialise condition array dict for each permutation
                    grp_set_index = str(merged_set_index).split("-")

                    for set_index, parentVar in zip(grp_set_index, parentVar_list):

                        parentVarBody = conditionalBody["parent_conditions"][parentVar] # get corresponding parent body
                        set_values = parentVarBody["condition_value"][int(set_index)] # get corresponding value from parent body, e.g. "1", "YES"
                        parentVarTransform_meta = cond_transformer.transformer_meta_dict[parentVar] # get meta information of how parentVar is transformed
                        parentVarTransform_meta_outputfields = parentVarTransform_meta['output_fields'].keys() # get list of parentVar output fields after transformation (including null)
                        sub_cond_array = None

                        # Build Sampling Conditions
                        if (parentVarBody['condition']=="set"):

                            if parentVarTransform_meta['transformer_type']=='One-Hot':
                                parentVarTransform_meta_params_dict = parentVarTransform_meta['params_dict']
                                for set_value in set_values:
                                    hotCol = parentVarTransform_meta_params_dict[set_value]
                                    if sub_cond_array is None:
                                        sub_cond_array = (samples[hotCol] == samples[parentVarTransform_meta_outputfields].max(axis=1))
                                    else:
                                        sub_cond_array = sub_cond_array | (samples[hotCol] == samples[parentVarTransform_meta_outputfields].max(axis=1))

                            elif parentVarTransform_meta['transformer_type'] == 'LabelEncoding':
                                parentVarTransform_meta_params_dict = parentVarTransform_meta['params_dict']
                                parentVar_value = list(parentVarTransform_meta_outputfields)[0] #<parentVar>.value
                                for set_value in set_values:
                                    label_en = parentVarTransform_meta_params_dict[set_value]
                                    if sub_cond_array is None:
                                        sub_cond_array = (samples[parentVar_value].round(0) == label_en)
                                    else:
                                        sub_cond_array = sub_cond_array | (samples[parentVar_value].round(0) == label_en)

                            elif parentVarTransform_meta['transformer_type'] == 'Cat1':
                                parentVarTransform_meta_interval_dict = parentVarTransform_meta['intervals']
                                parentVar_value = list(parentVarTransform_meta_outputfields)[0] #<parentVar>.value
                                temp_rev_col = samples[parentVar_value].apply(lambda x: next(key for key, (lower, upper) in parentVarTransform_meta_interval_dict.items() if lower <= x <= upper))
                                for set_value in set_values:
                                    if sub_cond_array is None:
                                        sub_cond_array = (temp_rev_col == set_value)
                                    else:
                                        sub_cond_array = sub_cond_array | (temp_rev_col == set_value)

                        elif (parentVarBody['condition']=="range"):
                            parentVar_value = list(parentVarTransform_meta_outputfields)[0] #<parentVar>.value
                            for set_value in set_values:
                                if sub_cond_array is None:
                                    sub_cond_array = eval(f"(samples[parentVar_value]{set_value})")
                                else:
                                    sub_cond_array = sub_cond_array & eval(f"(samples[parentVar_value]{set_value})")

                        
                        if cond_array[merged_set_index] is None:
                            cond_array[merged_set_index] = sub_cond_array
                        else:
                            cond_array[merged_set_index] = cond_array[merged_set_index] & sub_cond_array

                    # Filter Full Samples for Required Parent Conditions
                    if (cond_array[merged_set_index] is None):
                        sampling_condition_array = None
                    else:
                        sampling_condition_array = samples.loc[cond_array[merged_set_index]]

                    if (self.debug):
                        print(f"Filtered Samples Based on Condition: {set_no}:{merged_set_index} \n: {sampling_condition_array}")

                    if (sampling_condition_array is not None):
                        # Drop Children from Full-Samples
                        sampling_condition_array = sampling_condition_array.drop(
                            columns = childVarTransform_meta_outputfields,
                            errors = 'ignore'
                        )

                        # Get Conditional Copula
                        gaussian_copula_conditional = self.storage['cond_copula'][set_no][merged_set_index]

                        # Build Covariates
                        # Filtering non-parent variables to use as covariates to generate children variables
                        conditions_Array = []
                        if "conditions_var" in conditionalBody:
                            conditions_var = conditionalBody['conditions_var']
                            if (type(conditions_var) is list):
                                if (self.debug):
                                    print(f"Covariates List = {conditions_var}")

                                for c_var in conditions_var:
                                    a = cond_transformer.transformer_meta_dict[c_var]['output_fields'].keys()
                                    conditions_Array.extend(list(a))

                            else: #number for thresholding correlation
                                if (self.debug):
                                    print(f"Covariates Threshold = {conditions_var}")

                                for c_var in childVarTransform_meta_outputfields: #add all non-parent variables that exceed threshold as covariates
                                    cov_df = gaussian_copula_conditional.correlation[c_var].abs()
                                    new_cov_df = cov_df[(cov_df>=conditions_var)]
                                    conditions_Array.extend(list(new_cov_df.index))

                            conditions_Array = list(set(conditions_Array)) # remove duplicates

                            for c_var in childVarTransform_meta_outputfields: # remove all children variables as covariates
                                if c_var in conditions_Array:
                                    conditions_Array.remove(c_var)

                        if (self.debug):
                            print(f"Covariates Used for Sampling: {conditions_Array}")


                        # Resample Selected Rows
                        ii = 1
                        for s_index, s_row in sampling_condition_array.iterrows():

                            # build conditions from covariates
                            if (len(conditions_Array) == 0):
                                conditions = None
                            else:
                                s_row_e = s_row[conditions_Array]
                                conditions = s_row_e.to_dict()

                            if (self.debug):
                                print(conditions)
                            cond_samples = gaussian_copula_conditional.sample(size=1, conditions=conditions)

                            if (self.debug):
                                print(ii)
                                print(s_index)
                                # print(cond_samples.iloc[0][conditions_Array])
                                print(cond_samples.iloc[0][childVarTransform_meta_outputfields])

                            
                            samples.loc[s_index,childVarTransform_meta_outputfields] = cond_samples.iloc[0][childVarTransform_meta_outputfields]
                            ii += 1

        # Save generated samples
        self.syn_samples_conditional_df = deepcopy(samples)

        # Output to file
        self._save_data_to_file(self.syn_samples_conditional_df, self.output_filenames['conditional_synthetic_samples'])

    def syn_generate(self, sample_size=2000, cond_bool=False, conditions=None):

        # Transformation
        try:
            self.transform(metaData=self.metaData_transformer, var_list=self.var_list_filter)
            if cond_bool:
                self.transform_conditional(metaData=self.metaData_transformer)

        except ValueError as e:
            raise ValueError('Error performing transformation: ' + str(e)) from None
        
        # Check there are variables left after filtering for chosen variables
        if len(self.storage['transformer'].var_list) == 0:
            raise ValueError('No variables left to transform after filtering.')
        
        # Fit Copula
        try:
            self.fit_gaussian_copula()
            if cond_bool:
                self.fit_gaussian_copula_conditional()
        except ValueError as e:
            raise ValueError('Error fitting copula: ' + str(e)) from None
        
        # Sample Copula
        try:
            self.sample_gaussian_copula(sample_size=sample_size, conditions=conditions)
            if cond_bool:
                self.sample_gaussian_copula_conditional()
        except ValueError as e:
            raise ValueError('Error sampling from fitted copula: ' + str(e)) from None
        
        # Reverse Transformation
        try:
            self.reverse_transform()
        except ValueError as e:
            raise ValueError('Error reversing transform: ' + str(e)) from None
        
        return True
    
    def build_privacyMetric(self):

        ori = self.reversed_transformed_df
        syn = self.reversed_df
        syn_cond = self.reversed_conditional_df
        control = self.reversed_control_df

        ori = ut_.convert_datatypes(ori)
        syn = ut_.convert_datatypes(syn)
        syn_cond = ut_.convert_datatypes(syn_cond)
        control = ut_.convert_datatypes(control)

        privacyMetric = PM(ori=ori, syn=syn, control=control)
        privacyMetric_conditional = PM(ori=ori, syn=syn_cond, control=control)

        self.privacyMetricEval = privacyMetric
        self.privacyMetricEval_cond = privacyMetric_conditional

        return True
    
    def privacyMetric_singlingOut_Batch(self, n=None, mode='univariate', n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Singling Out Evaluator, batch process, n={n}, mode={mode}, Standard Copula...")

        # Running batch wrapper for singling out
        if mode == 'univariate':
            pathDir = self.output_filenames["singlingOut_uni_samples"]
        elif mode == 'multivariate':
            pathDir = self.output_filenames["singlingOut_multi_samples"]
        singlingOut_standard_filename = ut_.update_filename_with_suffix(pathDir, f'n={n}')

        res = self.privacyMetricEval.singlingOut_batch(
            outputcsv_filename=singlingOut_standard_filename,
            n_attacks=n_attacks,
            mode=mode,
            print_results=print_results,
            batch_n=n
        )

        # Save results
        self.privacyMetricResults["singlingOut_standard"] = res

        return res
    
    def privacyMetric_singlingOut_cond_Batch(self, n=None, mode='univariate', n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Singling Out Evaluator, batch process, n={n}, mode={mode}, Conditional Copula...")

        # Running batch wrapper for singling out
        if mode == 'univariate':
            pathDir = self.output_filenames["conditional_singlingOut_uni_samples"]
        elif mode == 'multivariate':
            pathDir = self.output_filenames["conditional_singlingOut_multi_samples"]
        singlingOut_conditional_filename = ut_.update_filename_with_suffix(pathDir, f'n={n}')

        res_cond = self.privacyMetricEval_cond.singlingOut_batch(
            outputcsv_filename=singlingOut_conditional_filename,
            n_attacks=n_attacks,
            mode=mode,
            print_results=print_results,
            batch_n=n
        )

        # Save results
        self.privacyMetricResults["singlingOut_conditional"] = res_cond

        return res_cond
    
    def privacyMetric_Linkability_Batch(self, aux_cols, n_neighbors=10, n=None, n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Linkability Evaluator, batch process, n={n}, Standard Copula...")
        
        # Running batch wrapper for linkability
        pathDir = self.output_filenames["linkability_samples"]
        linkability_standard_filename = ut_.update_filename_with_suffix(pathDir, f'n={n}-n_neighbors={n_neighbors}')

        res = self.privacyMetricEval.linkability_batch(
            aux_cols=aux_cols,
            n_neighbors=n_neighbors,
            outputcsv_filename=linkability_standard_filename,
            n_attacks=n_attacks,
            print_results=print_results,
            batch_n=n
        )

        # Save results
        self.privacyMetricResults["linkability_standard"] = res

        return res
    
    def privacyBatch_Linkability_cond_Batch(self, aux_cols, n_neighbors=10, n=None, n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Linkability Evaluator, batch process, n={n}, Conditional Copula...")

        # Running batch wrapper for linkability conditional
        cond_pathDir = self.output_filenames["conditional_linkability_samples"]
        linkability_conditional_filename = ut_.update_filename_with_suffix(cond_pathDir, f'n={n}-n_neighbors={n_neighbors}')

        res_cond = self.privacyMetricEval_cond.linkability_batch(
            aux_cols=aux_cols,
            n_neighbors=n_neighbors,
            outputcsv_filename=linkability_conditional_filename,
            n_attacks=n_attacks,
            print_results=print_results,
            batch_n=n
        )

        # Save results
        self.privacyMetricResults["linkability_conditional"] = res_cond

        return res_cond

    
    def privacyMetric_Inference_Batch(self, n=None, n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Inference Evaluator, batch process, n={n}, Standard Copula...")
        
        # Running batch wrapper for inference
        pathDir = self.output_filenames["inference_samples"]
        inference_standard_filename = ut_.update_filename_with_suffix(pathDir, f"n={n}")
        res = self.privacyMetricEval.inference_batch(
            outputcsv_filename_prefix=inference_standard_filename,
            n_attacks=n_attacks,
            print_results=print_results,
            batch_n = n
        )

        # Save results
        self.privacyMetricResults["inference_standard"] = res

        return res
    
    def privacyMetric_Inference_cond_Batch(self, n=None, n_attacks='auto', print_results=True):

        if n is None:
            n = self.privacy_batch_n

        if (self.debug):
            print(f"Running Inference Evaluator, batch process, n={n}, Conditional Copula...")
        
        # Running batch wrapper for inference
        cond_pathDir = self.output_filenames["conditional_inference_samples"]
        inference_conditional_filename = ut_.update_filename_with_suffix(cond_pathDir, f"n={n}")
        res_cond = self.privacyMetricEval_cond.inference_batch(
            outputcsv_filename_prefix=inference_conditional_filename,
            n_attacks=n_attacks,
            print_results=print_results,
            batch_n=n
        )

        # Save results
        self.privacyMetricResults["inference_conditional"] = res_cond

        return res_cond



    def build_storage(self):
        self.storage = {}
        self.storage['transformer'] = None
        self.storage['copula'] = None

        # Conditional Storage
        self.storage['cond_transformer'] = {}
        self.storage['cond_copula'] = {}

    def build_filenames(self):

        # Build Output Filename (with designated Prefix)
        self.output_filename_withprefix = ut_.update_filename_with_suffix(self.trainxlsx, self.output_general_prefix)

        self.output_filenames = {}

        # For class instance
        class_instance_filename_suffix = "CL"
        class_instance_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, class_instance_filename_suffix)
        class_instance_filename = ut_.change_extension(class_instance_filename, self.output_type_obj)
        class_instance_filename = self.syn_data_path + class_instance_filename
        self.output_filenames["tc-class-instance"] = class_instance_filename

        # For class instance outputfilenames
        class_outputfilenames_filename_suffix = "CL-OF"
        class_outputfilenames_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, class_outputfilenames_filename_suffix)
        class_outputfilenames_filename = ut_.change_extension(class_outputfilenames_filename, self.output_type_data)
        class_outputfilenames_filename = self.syn_data_path + class_outputfilenames_filename
        self.output_filenames["tc-class-outputfilenames"] = class_outputfilenames_filename

        # For Curated Data prior to Transformation
        curated_filename_suffix = "CURATED"
        curated_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, curated_filename_suffix)
        curated_filename = ut_.change_extension(curated_filename, self.output_type_data)
        curated_filename = self.syn_data_path + curated_filename
        self.output_filenames["curated"] = curated_filename

        # For Transformed Data
        transformed_filename_suffix = "TRANSFORMED"
        transformed_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, transformed_filename_suffix)
        transformed_filename = ut_.change_extension(transformed_filename, self.output_type_data)
        transformed_filename = self.syn_data_path + transformed_filename
        self.output_filenames["transformed"] = transformed_filename

        # For Control Data (for privacy leakage testing)
        control_filename_suffix = "CONTROL"
        control_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, control_filename_suffix)
        control_filename = ut_.change_extension(control_filename, self.output_type_data)
        control_filename = self.syn_data_path + control_filename
        self.output_filenames["control"] = control_filename

        # For Synthetic Data (before reversal)
        synthetic_filename_suffix = "SYN"
        synthetic_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, synthetic_filename_suffix)
        synthetic_filename = ut_.change_extension(synthetic_filename, self.output_type_data)
        synthetic_filename = self.syn_data_path + synthetic_filename
        self.output_filenames["synthetic_samples"] = synthetic_filename

        # For Reversed Transformed Data (synthetic data after reversal)
        reversed_filename_suffix = "REV"
        reversed_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, reversed_filename_suffix)
        reversed_filename = ut_.change_extension(reversed_filename, self.output_type_data)
        reversed_filename = self.syn_data_path + reversed_filename
        self.output_filenames["reversed_samples"] = reversed_filename

        # For Reversed Controlled Data (note: there's really no need to transform and then reverse control data, except for further experiments on control data's copula)
        control_reversed_filename_suffix = "CONTROLREV"
        control_reversed_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, control_reversed_filename_suffix)
        control_reversed_filename = ut_.change_extension(control_reversed_filename, self.output_type_data)
        control_reversed_filename = self.syn_data_path + control_reversed_filename
        self.output_filenames["controlReversed_samples"] = control_reversed_filename

        # For Training data
        training_filename_suffix = "TRAINING"
        training_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, training_filename_suffix)
        training_filename = ut_.change_extension(training_filename, self.output_type_data)
        training_filename = self.syn_data_path + training_filename
        self.output_filenames["training_samples"] = training_filename

        # For Singling Out Privacy Leakage Test (Univariate)
        singlingOut_suffix = "SINGLINGOUT_UNI"
        singlingOut_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, singlingOut_suffix)
        singlingOut_filename = ut_.change_extension(singlingOut_filename, 'csv')
        singlingOut_filename = self.privacyMetrics_path + singlingOut_filename
        self.output_filenames["singlingOut_uni_samples"] = singlingOut_filename

        # For Singling Out Privacy Leakage Test (Multivariate)
        singlingOut_multi_suffix = "SINGLINGOUT_MULTI"
        singlingOut_multi_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, singlingOut_multi_suffix)
        singlingOut_multi_filename = ut_.change_extension(singlingOut_multi_filename, 'csv')
        singlingOut_multi_filename = self.privacyMetrics_path + singlingOut_multi_filename
        self.output_filenames["singlingOut_multi_samples"] = singlingOut_multi_filename

        # For Linkability Privacy Leakage Test
        linkability_suffix = "LINKABILITY"
        linkability_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, linkability_suffix)
        linkability_filename = ut_.change_extension(linkability_filename, 'csv')
        linkability_filename = self.privacyMetrics_path + linkability_filename
        self.output_filenames["linkability_samples"] = linkability_filename

        # For Inference Privacy Leakage Test
        inference_suffix = "INFERENCE"
        inference_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, inference_suffix)
        inference_filename = ut_.change_extension(inference_filename, 'csv')
        inference_filename = self.privacyMetrics_path + inference_filename
        self.output_filenames["inference_samples"] = inference_filename
        

        # Conditional Stuff
        self.set_index_permutations_dict = {}
        self.output_filenames["conditional_transformed"] = {}

        if self.conditionalSettings_dict is not None:
            for set_no, conditionalBody in self.conditionalSettings_dict.items():
                if (conditionalBody["bool"]):
                    if "parent_conditions" in conditionalBody:
                        
                        # Build Conditional Set-Index (build permutations)
                        full_list_set_index = self._conditional_makeSetIndex(conditionalBody["parent_conditions"])
                        self.set_index_permutations_dict[set_no] = full_list_set_index # store for future use
                        self.output_filenames['conditional_transformed'][set_no] = {}

                        for merged_set_index in full_list_set_index: # e.g. "1-1-1", "1-2-1"

                            # Transformed Data
                            clean_str_suffix = ut_.clean_filename_str(str(set_no) + "-" + str(merged_set_index))
                            transformed_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, clean_str_suffix)
                            transformed_filename = ut_.update_filename_with_suffix(transformed_filename, transformed_filename_suffix)
                            transformed_filename = ut_.change_extension(transformed_filename, self.output_type_data)
                            transformed_filename = self.syn_data_path + transformed_filename
                            self.output_filenames['conditional_transformed'][set_no][merged_set_index] = transformed_filename

            # For CONDITIONAL Synthetic Data (before reversal)
            conditional_synthetic_filename_suffix = "COND_SYN"
            conditional_synthetic_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_synthetic_filename_suffix)
            conditional_synthetic_filename = ut_.change_extension(conditional_synthetic_filename, self.output_type_data)
            conditional_synthetic_filename = self.syn_data_path + conditional_synthetic_filename
            self.output_filenames["conditional_synthetic_samples"] = conditional_synthetic_filename

            # For Reversed Transformed Data (conditional synthetic data reversal)
            conditional_reversed_filename_suffix = "COND_REV"
            conditional_reversed_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_reversed_filename_suffix)
            conditional_reversed_filename = ut_.change_extension(conditional_reversed_filename, self.output_type_data)
            conditional_reversed_filename = self.syn_data_path + conditional_reversed_filename
            self.output_filenames["conditional_reversed_samples"] = conditional_reversed_filename

            # For Singling Out Privacy Leakage Test (Univariate)
            conditional_singlingOut_suffix = "COND_SINGLINGOUT_UNI"
            conditional_singlingOut_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_singlingOut_suffix)
            conditional_singlingOut_filename = ut_.change_extension(conditional_singlingOut_filename, 'csv')
            conditional_singlingOut_filename = self.privacyMetrics_path + conditional_singlingOut_filename
            self.output_filenames["conditional_singlingOut_uni_samples"] = conditional_singlingOut_filename

            # For Singling Out Privacy Leakage Test (Multivariate)
            conditional_singlingOut_multi_suffix = "COND_SINGLINGOUT_UNI"
            conditional_singlingOut_multi_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_singlingOut_multi_suffix)
            conditional_singlingOut_multi_filename = ut_.change_extension(conditional_singlingOut_multi_filename, 'csv')
            conditional_singlingOut_multi_filename = self.privacyMetrics_path + conditional_singlingOut_multi_filename
            self.output_filenames["conditional_singlingOut_multi_samples"] = conditional_singlingOut_multi_filename

            # For Linkability Privacy Leakage Test
            conditional_linkability_suffix = "COND_LINKABILITY"
            conditional_linkability_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_linkability_suffix)
            conditional_linkability_filename = ut_.change_extension(conditional_linkability_filename, 'csv')
            conditional_linkability_filename = self.privacyMetrics_path + conditional_linkability_filename
            self.output_filenames["conditional_linkability_samples"] = conditional_linkability_filename

            # For Inference Privacy Leakage Test
            conditional_inference_suffix = "COND_INFERENCE"
            conditional_inference_filename = ut_.update_filename_with_suffix(self.output_filename_withprefix, conditional_inference_suffix)
            conditional_inference_filename = ut_.change_extension(conditional_inference_filename, 'csv')
            conditional_inference_filename = self.privacyMetrics_path + conditional_inference_filename
            self.output_filenames["conditional_inference_samples"] = conditional_inference_filename

            self.conditional_set_bool = True


    def _save_data_to_file(self, df, filename, indexTrue=False, sheetname="Sheet1"):
        """
        Saves a dataframe to file based on the file extension of the given filename.
        Inputs:
            df (pandas.dataframe): a pandas dataframe to be saved to file.
            filename (string): the name of the file to save the dataframe to.
            indexTrue (boolean): whether to save the index of the DF. Default is False
            sheetname (string, optional): The name of the sheet to save the dataframe on, only applicable for xlsx file extensions. Default is "Sheet1". 

        Returns:
            None

        Raises:
            ValueError: If the file extension is not supported.
        """

        file_ext = ut_.get_extension(filename)

        if (file_ext=='csv'):
            ut_.save_df_as_csv(df, filename, index=indexTrue)

        elif (file_ext=='xlsx'):
            ut_.save_df_as_excel(df, 
                excel_file_name = filename, 
                sheet_name = sheetname,
                index = indexTrue # not saving the index (if False)
            )

        else:
            raise ValueError(f"Not able to save data to file for extension type: {file_ext}")
        
        return True
        
    def save(self):
        """Saves the current class instance to a pickle file. Saves the output filenames dictionary to a csv file."""

        b = self.save_instance()
        c = self.save_outputFilenames()

        if b and c:
            return True

        return False
    
    def save_instance(self):
        """Saves the current class instance to a pickle file.
        Inputs:
            self: current class instance
        Returns:
            True if the class instance is successfully saved to the pickle file, False otherwise.
        """

        print(f"Saving class instance to filename: {self.output_filenames['tc-class-instance']}")

        b = self._save_to_pickle(self, self.output_filenames['tc-class-instance'])
        if b:
            print(f"Saving class instance complete.")
        else:
            print(f"Saving class instance failed.")

        return b
    
    def save_outputFilenames(self):
        """Saves the output filenames dictionary to a csv file
        """

        print(f"Saving output filenames to csv: {self.output_filenames['tc-class-outputfilenames']}")
        
        # Convert output filenames dictionary to dataframe
        df = pd.DataFrame.from_dict(self.output_filenames, orient='index', columns=['Object'])
        df['Type'] = df.index

        # Save dataframe to csv file
        b = self._save_data_to_file(df, self.output_filenames['tc-class-outputfilenames'], indexTrue=False)
        if b:
            print("Saving output filenames complete.")
        else:
            print("Saving output filenames failed.")

        return True

    def _save_to_pickle(self, toSave, filename):
        """Saves the given object to a pickle file.
        
        Inputs:
            toSave: Object to be saved to the pickle file
            filename: name of the pickle file to be created

        Returns:
            True if the object is successfully saved to the pickle file. False otherwise.
        """

        try:
            pk_filename = open(filename, "wb")
            pickle.dump(toSave, pk_filename)
            pk_filename.close()

            return True
        
        except Exception as e:
            print("Error saving pickle file: {}".format(e))

        return False

    def _conditional_makeSetIndex(self, parent_conditions):
        """Build reference index set for parent conditions (used for conditional copula).
        Inputs:
            parent_conditions (dict): dictionary of parent conditions (follow template):
            E.g.
            "parent_conditions": {
                "SurveyYr": {
                    "condition": "set",
                    "condition_value": {
                        1: ["2009_10"],
                        2: ["2011_12"]
                    }
                },
                "Age": {
                    "condition": "range",
                    "condition_value": {
                        1: [">=3", "<80"],
                        2: ["<3"],
                        3: [">=80"],
                        # 4: ["<80"]
                    }
                }
            },
        Output:
            list_set_index (list): list of index set
            E.g. ['1-1', '1-2', '1-3', '2-1', '2-2', '2-3']
        """

        list_set_index = []
        for parentVar, parentVarBody in parent_conditions.items():
            second_list = list(parentVarBody["condition_value"].keys())
            B = []
            if (len(list_set_index)==0):
                # B = second_list
                B = [str(x) for x in second_list]
            else:
                for a in list_set_index:
                    for b in second_list:
                        B.append(str(a) + "-" + str(b))
            list_set_index = deepcopy(B)

        return list_set_index
    
    def _conditional_update_newNullValue(self, childVarList, transformed_filtered):
        """Given a transformed dataframe that has been filtered based on parent conditions (transformed_filtered), loop through a list of child variables (childVarList) and update the 'null' values with the new 'mean'/'mode'/'median'.

        Output: df (transformed_filtered with updated null values)
        """

        # Get meta information from Transformer
        transformer_meta_dict = self.storage['transformer'].transformer_meta_dict # transformer outputs
        metaData = self.storage['transformer'].metaData # user inputs to transformer

        # Loop through the list of child variables
        for childVar in childVarList:
            if (transformer_meta_dict[childVar]['transformer_type'] == 'Numerical'):
                if (transformer_meta_dict[childVar]['null']['fix_null']):

                    childVar_t_name = childVar + ".value"
                    childVar_t_null_name = childVar + ".is_null"

                    if (childVar_t_null_name in transformed_filtered.columns):
                        cond_i6 = transformed_filtered[childVar_t_null_name] == 1 # the null indicator

                        # Learn the new value for replacing null
                        if (metaData[childVar]['null'] == 'mean'):
                            new_null_value = transformed_filtered[~cond_i6][childVar_t_name].mean()
                        elif (metaData[childVar]['null'] == 'mode'):
                            new_null_value = transformed_filtered[~cond_i6][childVar_t_name].mode(dropna=True)[0]
                        elif (metaData[childVar]['null'] == 'median'):
                            new_null_value = transformed_filtered[~cond_i6][childVar_t_name].median()
                        else:
                            new_null_value = metaData[childVar]['null']

                        # Replace null with new value
                        if (pd.isna(new_null_value)):
                            pass
                        else:
                            transformed_filtered.loc[cond_i6,[childVar_t_name]] = float(new_null_value)

        return transformed_filtered