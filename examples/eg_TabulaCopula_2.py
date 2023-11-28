# This example demonstrates the use of the TabulaCopula class to generate synthetic data for a multivariate real dataset (NHANES), between variables of known linear relationship.
# Added complications:
#  - the dataset has a large number of missing values

# LOAD DEPENDENCIES
import pprint, sys, os
import matplotlib.pyplot as plt
import pandas as pd

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.TabulaCopula import TabulaCopula

# LOAD DEFINITIONS
import definitions_nhanes_1 as defi

# SCRIPT SETTINGS
syn_data_bool = True # generate synthetic data
visual_bool = True # generate plots
cond_bool = True # generate synthetic data using conditional copula
output_general_prefix = 'TC2-C' # to label different runs

# INITIALISE metaData Transformer_dict
metaData_transformer = {
    'SurveyYr':{
        'null': "N.A.",
        'transformer_type': 'One-Hot' # or 'LabelEncoding'
    },
    'Age':{'null': 'ignore'},
    'AgeMonths':{'null': 'ignore'} #AgeMonths have large numbers of missing values. Using 'mean'/'mode' options is not recommended as the imputed values will distort the marginal distribution.
}
var_list = ['SurveyYr', 'Age', 'AgeMonths']

# INITIALISE conditional settings
if cond_bool:
    conditionalSettings_dict = {
        "set_1": {
            "bool": True,
            "parent_conditions": { # 2 parents
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
            "conditions_var": ["Age"],
            "children": ['AgeMonths']
        }
    }
else:
    conditionalSettings_dict = None

# GENERATE SYNTHETIC DATA
if syn_data_bool:

    # INITIALISE THE TABULACOPULA CLASS
    tc = TabulaCopula(
        definitions = defi,
        output_general_prefix = output_general_prefix,
        var_list_filter = var_list,
        metaData_transformer = metaData_transformer,
        conditionalSettings_dict = conditionalSettings_dict,
        removeNull = False, #when False, will NOT remove null values prior to transformation
        debug = True
    )

    # GENERATE SYNTHETIC DATA
    tc.syn_generate(cond_bool=cond_bool)

# VISUALISATION
if visual_bool:

    from bdarpack import VIsualPlot as vp

    data_df_filename = f"{dir_path}/synData/nhanes_raw-DD-CON-ST-{output_general_prefix}-CURATED.csv"
    syn_samples_df_filename = f"{dir_path}/synData/nhanes_raw-DD-CON-ST-{output_general_prefix}-REV.csv"
    syn_samples_conditional_df_filename = f"{dir_path}/synData/nhanes_raw-DD-CON-ST-{output_general_prefix}-COND_REV.csv"

    data_df = pd.read_csv(data_df_filename)
    syn_samples_df = pd.read_csv(syn_samples_df_filename)
    if cond_bool:
        syn_samples_conditional_df = pd.read_csv(syn_samples_conditional_df_filename)


    # Plot Correlation Plots
    ax_corr_1, ax_corr_2, fig_corr = vp.corrMatrix_compare(data_df, syn_samples_df)
    if cond_bool:
        ax_corr_cond_1, ax_corr_cond_2, fig_cond_corr = vp.corrMatrix_compare(data_df, syn_samples_conditional_df)
    
    # Plot Histogram of Data Sample
    
    if cond_bool:
        ax_hist, fig_histogram = vp.hist_compare(data_df, syn_samples_df, var_list=var_list, no_cols=3)
        ax_cond_hist, fig_cond_histogram = vp.hist_compare(data_df, syn_samples_conditional_df, var_list=var_list, no_cols=3)
    else: 
        ax_hist, fig_histogram = vp.hist_compare(data_df, syn_samples_df, var_list=var_list, no_cols=3)

    # Plot Scatter
    data_df_surveyYr_2009_10 = data_df[data_df['SurveyYr']=='2009_10']
    data_df_surveyYr_2011_12 = data_df[data_df['SurveyYr']=='2011_12']
    syn_samples_df_surveyYr_2009_10 = syn_samples_df[syn_samples_df['SurveyYr']=='2009_10']
    syn_samples_df_surveyYr_2011_12 = syn_samples_df[syn_samples_df['SurveyYr']=='2011_12']

    ax_scatter, fig_scatter = vp.scatterPlot(data_df_surveyYr_2009_10['Age'], data_df_surveyYr_2009_10['AgeMonths'], fig=plt.figure(), color='blue', marker='.', label='Real (2009_10)')
    ax_scatter, fig_scatter = vp.scatterPlot(data_df_surveyYr_2011_12['Age'], data_df_surveyYr_2011_12['AgeMonths'], fig=fig_scatter, ax=ax_scatter, color='red', marker='.', label='Real (2011_12)')

    ax_scatter, fig_scatter = vp.scatterPlot(syn_samples_df_surveyYr_2009_10['Age'], syn_samples_df_surveyYr_2009_10['AgeMonths'], fig=fig_scatter, ax=ax_scatter, color='grey', marker='x', label='Syn (2009_10)')
    ax_scatter, fig_scatter = vp.scatterPlot(syn_samples_df_surveyYr_2011_12['Age'], syn_samples_df_surveyYr_2011_12['AgeMonths'], fig=fig_scatter, ax=ax_scatter, color='black', marker='x', label='Syn (2011_12)')

    if cond_bool:
        syn_samples_conditional_df_surveyYr_2009_10 = syn_samples_conditional_df[syn_samples_conditional_df['SurveyYr']=='2009_10']
        syn_samples_conditional_df_surveyYr_2011_12 = syn_samples_conditional_df[syn_samples_conditional_df['SurveyYr']=='2011_12']

        ax_scatter_cond, fig_scatter_cond = vp.scatterPlot(data_df_surveyYr_2009_10['Age'], data_df_surveyYr_2009_10['AgeMonths'], fig=plt.figure(), color='blue', marker='.', label='Real (2009_10)')
        ax_scatter_cond, fig_scatter_cond = vp.scatterPlot(data_df_surveyYr_2011_12['Age'], data_df_surveyYr_2011_12['AgeMonths'], fig=fig_scatter_cond, ax=ax_scatter_cond, color='red', marker='.', label='Real (2011_12)')

        ax_scatter_cond, fig_scatter_cond = vp.scatterPlot(syn_samples_conditional_df_surveyYr_2009_10['Age'], syn_samples_conditional_df_surveyYr_2009_10['AgeMonths'], fig=fig_scatter_cond, ax=ax_scatter_cond, color='grey', marker='x', label='Syn-Cond (2009_10)')
        ax_scatter_cond, fig_scatter_cond = vp.scatterPlot(syn_samples_conditional_df_surveyYr_2011_12['Age'], syn_samples_conditional_df_surveyYr_2011_12['AgeMonths'], fig=fig_scatter_cond, ax=ax_scatter_cond, color='black', marker='x', label='Syn-Cond (2011_12)')

    plt.show()