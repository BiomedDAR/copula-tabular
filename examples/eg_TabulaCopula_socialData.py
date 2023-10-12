# This example demonstrates the use of the TabulaCopula class to generate synthetic data between variables of non-monotonic relationship.

# LOAD DEPENDENCIES
import sys, os
import matplotlib.pyplot as plt
import pickle

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from mz.TabulaCopula import TabulaCopula
from mz import VIsualPlot as vp
from mz import utils_ as ut_

# LOAD DEFINITIONS
import definitions_tc_sim_3 as defi

# SCRIPT SETTINGS
syn_data_bool = True # generate synthetic data
visual_bool = True # generate plots
cond_bool = True # generate synthetic data using conditional copula
output_general_prefix = 'TC3-C' # to label different runs


# INITIALISE conditional settings
if cond_bool:
    # LOAD CONDITIONAL SETTINGS
    conditionalSettings_dict = {
        "set_1-0": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": ut_.gen_dict_range_interval(interval=10, min_num=30, max_num=90)
                }
            },
            "conditions_var": ["Age"],
            "children": "allOthers"
        },
        "set_1-1": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": ut_.gen_dict_range_interval(interval=5, min_num=30, max_num=90)
                }
            },
            "conditions_var": ["Age"],
            "children": ["Asset"]
        },
        "set_1-2": {
            "bool": True,
            "parent_conditions": {
                "Age":{
                    "condition": "range",
                    "condition_value": { #intervals to tackle non-monotonicity of variables
                        1: [">=30", "<40"],
                        2: [">=40", "<50"],
                        3: [">=50", "<53"],
                        4: [">=53", "<73"],
                        5: [">=73", "<90"],
                    }
                }
            },
            "conditions_var": ["Age"],
            "children": ["Satisfaction"]
        }
    }
else:
    conditionalSettings_dict = None

if syn_data_bool:
    # INITIALISE metaData Transformer_dict
    metaData_transformer = {
        'AgeGroup':{
            'transformer_type': 'One-Hot'
        }
    }

    # INITIALISE THE TABULACOPULA CLASS
    tc = TabulaCopula(
        definitions = defi,
        output_general_prefix=output_general_prefix,
        conditionalSettings_dict = conditionalSettings_dict,
        metaData_transformer = metaData_transformer,
        debug=True
    )

    # GENERATE and SAVE SYNTHETIC DATA
    tc.syn_generate(cond_bool=cond_bool)
    tc.save()

# VISUALISATION
if visual_bool:
    if not syn_data_bool: #Load saved TC

        tc_filename = f"{dir_path}/synData/socialdata-{output_general_prefix}-CL.pkl"
        with open(tc_filename, 'rb') as fl:
            tc = pickle.load(fl)

    data_df = tc.train_df
    syn_samples_df = tc.reversed_df
    syn_samples_conditional_df = tc.reversed_conditional_df
    var_list = list(data_df.columns)

    # Plot Histogram of Data Sample
    if cond_bool:
        ax_hist, fig_histogram = vp.hist_compare(data_df, syn_samples_df, var_list=var_list, no_cols=3)
        ax_cond_hist, fig_cond_histogram = vp.hist_compare(data_df, syn_samples_conditional_df, var_list=var_list, no_cols=3)
    else:
        ax_hist, fig_histogram = vp.hist_compare(data_df, syn_samples_df, var_list=var_list, no_cols=2)

    # Plot Correlation Plots
    corr_options = {
        "x_label_rot": 45
    }
    ax_corr_1, ax_corr_2, fig_corr = vp.corrMatrix_compare(data_df, syn_samples_df, options=corr_options)
    if cond_bool:
        ax_corr_cond_1, ax_corr_cond_2, fig_cond_corr = vp.corrMatrix_compare(data_df, syn_samples_conditional_df, options=corr_options)

    # ScatterPlot
    ax_scatter, fig_scatter = vp.scatterPlot_multiple_compare(data_df, syn_samples_df, n_plot_cols=3, ref='autopermute')
    
    if cond_bool:
        ax_scatter_cond, fig_scatter_cond = vp.scatterPlot_multiple_compare(data_df, syn_samples_conditional_df, n_plot_cols=3, ref='autopermute')

    plt.show()