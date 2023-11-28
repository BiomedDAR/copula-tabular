# This example demonstrates the use of the TabulaCopula class to generate risk leakage statistics.
# Third-party package: Anonymeter is required. To install, use 'pip install anonymeter'

# LOAD DEPENDENCIES
import sys, os
import matplotlib.pyplot as plt

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from bdarpack.TabulaCopula import load_TC

# LOAD THE SAVED TabulaCopula instance from 'eg_TabulaCopula_1.py'
import definitions_tc_sim_2 as defi #this is the same definitions script as the one used in 'eg_TabulaCopula_1.py'

tc = load_TC(defi)

# SET FLAGS FOR TYPE OF PRIVACY LEAKAGE TEST TO CONDUCT
singlingOut_uni = defi.SINGLINGOUT_UNI
singlingOut_multi = defi.SINGLINGOUT_MULTI
Linkability = defi.LINKABILITY
Inference = defi.INFERENCE
singlingOut_uni = True
singlingOut_multi = False
Linkability = True
Inference = True

# BUILD THE PRIVACY METRIC EVALUATORS
tc.build_privacyMetric()
privacyMetric_standard = tc.privacyMetricEval #built evaluator for standard copula
privacyMetric_conditional = tc.privacyMetricEval_cond #built evaluator for conditional copula

# SET THE NUMBER OF ITERATIONS (For Batch Process)
n = 4 #to overwrite the PRIVACY_BATCH_N value in definitions

# RUNNING THE VARIOUS PRIVACY LEAKAGE ATTACKS
# Results will be saved int he privacyMetrics (or any other folder specified in definitions, under 'PRIV_PATH') folder
if singlingOut_uni:

    # Run the singlingOut attack 'n' times (for standard copula)
    result_df = tc.privacyMetric_singlingOut_Batch(n=n, mode='univariate', n_attacks='auto', print_results=True)

    # Plot Box-Plot of Results (standard)
    fig_uni, ax_uni = privacyMetric_standard.plot_risk_results(result_df, plot_title=f'Singling Out (Standard) - Univariate')

    # Run the singlingOut attack 'n' times (for conditional copula)
    result_cond_df = tc.privacyMetric_singlingOut_cond_Batch(n=n, mode='univariate', n_attacks='auto', print_results=True)
                                                             
    # Plot Box-Plot of Results (conditional)
    fig_uni_cond, ax_uni_cond = privacyMetric_conditional.plot_risk_results(result_cond_df, plot_title=f'Singling Out (Conditional) - Univariate')

if Linkability:

    # Set linkability attack settings (see Anonymeter for details)
    n_neighbors = 10
    aux_cols = [
        ['cat1_w', 'cat2_x', 'cat4_z'],
        ['cat3_y']
    ]

    # Run the linkability attack 'n' times (for standard copula)
    link_result_df = tc.privacyMetric_Linkability_Batch(aux_cols=aux_cols, n_neighbors=n_neighbors, n=n)

    # Plot Box-Plot of Results (standard)
    fig_link, ax_link = privacyMetric_standard.plot_risk_results(link_result_df, plot_title="Linkability (Standard)")

    # Run the linkability attack 'n' times (for conditional copula)
    link_cond_result_df = tc.privacyBatch_Linkability_cond_Batch(aux_cols=aux_cols, n_neighbors=n_neighbors, n=n)

    # Plot Box-Plot of Results (conditional)
    fig_link_cond, ax_link_cond = privacyMetric_conditional.plot_risk_results(link_cond_result_df, plot_title='Linkability (Conditional)')

if Inference:

    # Run the inference attack 'n' times (for standard copula)
    res = tc.privacyMetric_Inference_Batch()
    print(res)

    # Plot Box-Plot of Results 'R' (standard)
    fig, ax = privacyMetric_standard.plot_inference_risk_results(res, res_col='R', plot_title='Inference Evaluator (R) (Standard)')

    # Plot Box-Plot of Results 'Naive Attack' (standard)
    fig_cv, ax_cv = privacyMetric_standard.plot_inference_risk_results(res, res_col='naive_value', plot_title='Inference Evaluator (Naive) (Standard)')

    # Plot Box-Plot of Results 'Control Attack' (standard)
    fig_cv, ax_cv = privacyMetric_standard.plot_inference_risk_results(res, res_col='control_value', plot_title='Inference Evaluator (Control) (Standard)')

    # Plot Box-Plot of Results 'Main Attack' (standard)
    fig_cv, ax_cv = privacyMetric_standard.plot_inference_risk_results(res, res_col='main_value', plot_title='Inference Evaluator (Main) (Standard)')

    # Run the inference attack 'n' times (for conditional copula)
    res_cond = tc.privacyMetric_Inference_cond_Batch()

    # Plot Box-Plot of Results 'R' (conditional)
    fig_cond, ax_cond = privacyMetric_conditional.plot_inference_risk_results(res_cond, res_col='R', plot_title='Inference Evaluator (R) (Conditional)')

    # Plot Box-Plot of Results 'Naive Attack' (conditional)
    fig_cv_cond, ax_cv_cond = privacyMetric_conditional.plot_inference_risk_results(res_cond, res_col='naive_value', plot_title='Inference Evaluator (Naive) (Conditional)')

    # Plot Box-Plot of Results 'Control Attack' (conditional)
    fig_cv_cond, ax_cv_cond = privacyMetric_conditional.plot_inference_risk_results(res_cond, res_col='control_value', plot_title='Inference Evaluator (Control) (Conditional)')

    # Plot Box-Plot of Results 'Main Attack' (conditional)
    fig_cv_cond, ax_cv_cond = privacyMetric_conditional.plot_inference_risk_results(res_cond, res_col='main_value', plot_title='Inference Evaluator (Main) (Conditional)')

plt.show()