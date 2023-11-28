import pandas as pd
import numpy as np
from bdarpack import utils_ as ut_
from bdarpack import VIsualPlot as vp

from anonymeter.evaluators import SinglingOutEvaluator
from anonymeter.evaluators import LinkabilityEvaluator
from anonymeter.evaluators import InferenceEvaluator

class PrivacyMetric:
    """Wrapper for running privacy leakage metrics on tabular synthetic data. Include methods:
        (a) anonymeter
    """

    def __init__(self,
        ori,
        syn,
        control,
        debug = False
    ):
        self.debug = debug
        self.ori = ori
        self.syn = syn
        self.control = control

    
    def singlingOut(self, n_attacks='auto', mode='univariate', print_results=True):
        """
        Evaluates the privacy-preserving of the proposed system using the Singling Out attack.
        Parameters
        -------
        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size

        mode: str, optional (default='univariate')
            Mode of singling out attack to be used.
            Options are 'univariate' and 'multivariate'

        print_results: bool, optional (default=True)
            If True, the results of the attack are printed on the console.

        Returns
        -------
        res: EvaluationResult
            The result of the singling out attack. Contains the details like attack rate, baseline rate, control rate, and overall privacy risk score.
        """

        if (n_attacks=='auto'):
            n_attacks = min(2000, int(0.8 * len(self.syn)))
        elif type(n_attacks) != int:
            raise TypeError('n_attacks must be either "auto" or an integer.')

        evaluator = SinglingOutEvaluator(
            ori = self.ori,
            syn = self.syn,
            control = self.control,
            n_attacks = n_attacks
        )

        try:
            evaluator.evaluate(mode=mode)
            res = evaluator.results()

            if print_results:
                print("Number of Attacks:", n_attacks)
                print("Success rate of main attack:", res.attack_rate)
                print("Success rate of baseline attack:", res.baseline_rate)
                print("Success rate of control attack:", res.control_rate)
                print("Privacy Risk:", res.risk())

        except RuntimeError as ex:
            print(f"{mode} singling out evaluation failed with {ex}. Please re-run this cell."
                "For more stable results increase `n_attacks`. Note that this will make the evaluation slower.")
            
        # Saving the Evaluator for future use
        self.singlingOutEvaluator = evaluator

        return res
    
    def singlingOut_batch(self, outputcsv_filename='', n_attacks='auto', mode='univariate', print_results=True, batch_n=100):
        """
        Run the singling out attack in batch mode.
        Parameters
        -------
        outputcsv_filename: str, optional (default='')
            If provided, the results are saved in the csv file.
        
        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size.

        mode: str, optional (default='univariate')
            Mode of singling out attack to be used.
            Options are 'univariate' and 'multivariate'.

        print_results: bool, optional (default=True)
            If True, the results of each trial are printed on the console.

        batch_n: int, optional (default=100)
            Number of trials to run.

        Returns
        -------
        results_df: pd.DataFrame
            The data frame containing the results from all the trials in the batch. It contains main attack success rate, navie success rate, control success rate and privacy risk score for each trial.
        """

        if self.debug:
            print(f"Running Batch Process for Singling Out ({mode}).")

        results = {}
        
        for i in range(batch_n):
            print(f"Running Trial {i+1} out of {batch_n}")

            res = self.singlingOut(
                n_attacks = n_attacks, 
                mode = mode, 
                print_results = print_results
            )

            # Save res in results
            results[i] = {
                'main_value': res.attack_rate.value,
                'main_error': res.attack_rate.error,
                'naive_value': res.baseline_rate.value,
                'naive_error': res.baseline_rate.error,
                'control_value': res.control_rate.value,
                'control_error': res.control_rate.error,
                'R': res.risk().value
            }
        
        # Convert to dataframe
        results_df = pd.DataFrame(results).T

        # Save to CSV
        if outputcsv_filename != '':
            results_df.to_csv(outputcsv_filename, index=True)

        return results_df


    def linkability(self, aux_cols, n_neighbors, n_attacks='auto', print_results=True):
        """
        Evaluates the privacy-preserving statistics of the synthetic data using the Linkability attack.

        Parameters
        --------
        aux_cols: list
            List of column names of auxiliary columns used for linkability attack.
            E.g. aux_cols = [
                ['cat1_w', 'cat2_x', 'cat4_z'],
                ['cat3_y']
            ]

        n_neighbors: int
            Number of closest neighbors to check for a match.

        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size.

        print_results: bool, optional (default=True)
            If True, the results of the attack are printed on the console.

        Returns
        -------
        res: EvaluationResult
            The result of the linkability attack.
            It contains the details like attack rate, baseline rate, control rate, and overall privcy risk score.
        """

        if (n_attacks=='auto'):
            n_attacks = min(2000, int(0.8 * min(len(self.control),len(self.syn))))
        elif type(n_attacks) != int:
            raise TypeError('n_attacks must be either "auto" or an integer.')
        
        evaluator = LinkabilityEvaluator(
            ori = self.ori,
            syn = self.syn,
            control = self.control,
            n_attacks = n_attacks,
            aux_cols = aux_cols,
            n_neighbors = n_neighbors
        )

        try:
            evaluator.evaluate(n_jobs=-2) # n_jobs follow joblib convention. -1 = all cores, -2 = all execept one
            res = evaluator.results()

            if print_results:
                print("Number of Attacks:", n_attacks)
                print("Success rate of main attack:", res.attack_rate)
                print("Success rate of baseline attack:", res.baseline_rate)
                print("Success rate of control attack:", res.control_rate)
                print("Privacy Risk:", res.risk())

        except RuntimeError as ex:
            print(f"Linkability evaluation failed with {ex}. Please re-run this cell."
                "For more stable results increase `n_attacks`. Note that this will make the evaluation slower.")
            
        # Saving the Evaluator for future use
        self.linkabilityEvaluator = evaluator

        return res
    
    def linkability_batch(self, aux_cols, n_neighbors, n_attacks='auto', print_results=True, outputcsv_filename='', batch_n=100):
        """
        Evaluates the privacy-preserving of the proposed system using the Linkability attack, in batch mode.

        Parameters
        --------
        aux_cols: list
            List of column names of auxiliary columns used for linkability attack.
            E.g. aux_cols = [
                ['cat1_w', 'cat2_x', 'cat4_z'],
                ['cat3_y']
            ]
        
        n_neighbors: int
            Number of closest neighbors to check for a match

        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size.

        print_results: bool, optional (default=True)
            If True, the results of the attack are printed on the console.

        outputcsv_filename: str, optional (default='')
            The path of the csv file where the results should be saved to.
            If not provided, the results will not be saved to a csv file.

        batch_n: int, optional (default=100)
            Number of times the attack should be run.

        Returns
        ------
        results_df: pandas.DataFrame
            The results stored in a pandas.DataFrame object.
            It contains the details of each trial like attack rate, baseline rate, control rate, and overall privacy risk score.
        """

        if self.debug:
            print(f"Running Batch Process for Linkability Attack.")

        results = {}

        for i in range(batch_n):
            print(f"Running Trial {i+1} out of {batch_n}")

            res = self.linkability(
                aux_cols=aux_cols,
                n_neighbors=n_neighbors,
                n_attacks=n_attacks,
                print_results=print_results
            )

            # Save res in results
            results[i] = {
                'main_value': res.attack_rate.value,
                'main_error': res.attack_rate.error,
                'naive_value': res.baseline_rate.value,
                'naive_error': res.baseline_rate.error,
                'control_value': res.control_rate.value,
                'control_error': res.control_rate.error,
                'R': res.risk().value
            }

        # Convert to dataframe
        results_df = pd.DataFrame(results).T

        # Save to CSV
        if outputcsv_filename != '':
            results_df.to_csv(outputcsv_filename, index=True)

        return results_df
    
    def inference(self, n_attacks='auto', print_results=True):
        """
        Evaluates the privacy-preserving statistics of the synthetic data using the inference attack.

        Parameters
        -------
        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size.

        print_results: bool, optional (default=True)
            If True, the results of the attack are printed on the console.

        Returns
        ------
        results: list
            List of tuples containing the column name and the details of the inference attack on the specified column including attack rate, baseline rate, control rate, and overall privacy risk score.
        """

        if (n_attacks=='auto'):
            n_attacks = min(2000, int(0.8 * min(len(self.control),len(self.syn))))
        elif type(n_attacks) != int:
            raise TypeError('n_attacks must be either "auto" or an integer.')

        results = []
        columns = self.ori.columns
        for secret in columns:
            aux_cols = [col for col in columns if col!=secret] #what the attacker knows about its target

            evaluator = InferenceEvaluator(
                ori = self.ori,
                syn = self.syn,
                control = self.control,
                n_attacks = n_attacks,
                aux_cols = aux_cols,
                secret = secret
            )

            try:
                evaluator.evaluate(n_jobs=-2) # n_jobs follow joblib convention. -1 = all cores, -2 = all execept one
                res = evaluator.results()
                results.append((secret, res))

                if print_results:
                    print("Number of Attacks:", n_attacks)
                    print("Success rate of main attack:", res.attack_rate)
                    print("Success rate of baseline attack:", res.baseline_rate)
                    print("Success rate of control attack:", res.control_rate)
                    print("Privacy Risk:", res.risk())
            except RuntimeError as ex:
                print(f"Inference evaluation failed with {ex}. Please re-run this cell."
                    "For more stable results increase `n_attacks`. Note that this will make the evaluation slower.")
                
            # Saving the Evaluator for future use
            self.inferenceEvaluator = evaluator

        return results
    
    def inference_batch(self, outputcsv_filename_prefix='', n_attacks='auto', print_results=True, batch_n=100):
        """
        Evaluates the privacy-preserving properties of the synthetic data using the inference attack on multiple trials.

        Parameters
        -------
        outputcsv_filename_prefix: str, optional (default='')
            Prefix in the name of the csv used to save the results of the batch processing. filenames will be affixed with individual variable and saved separately.

        n_attacks: int or 'auto', optional (default='auto')
            Number of attacks to run on the data.
            If set to 'auto', it will be automatically set to 0.8 * dataset size

        print_results: bool, optional (default=True)
            If True, the results of the attack are printed on the console.

        batch_n: int, optional (default=100)
            Number of trials to evaluate the system.

        Returns
        -------
        results: dict
            Dictionary containing details of the inference attack of all columns in the dataset including attack rate, baseline rate, control rate, and overall privacy risk score across all trials.
        """

        if self.debug:
            print(f"Running Batch Process for Inference attack.")

        results = {}

        for i in range(batch_n):
            print(f"Running Trial {i+1} out of {batch_n}")

            res = self.inference(
                n_attacks = n_attacks,
                print_results = print_results
            )

            for res_i in res:
                if res_i[0] not in results:
                    results[res_i[0]] = {}
                
                results[res_i[0]][i] = {
                    'main_value': res_i[1].attack_rate.value,
                    'main_error': res_i[1].attack_rate.error,
                    'naive_value': res_i[1].baseline_rate.value,
                    'naive_error': res_i[1].baseline_rate.error,
                    'control_value': res_i[1].control_rate.value,
                    'control_error': res_i[1].control_rate.error,
                    'R': res_i[1].risk().value
                }

        # Save Results
        for secret in results.keys():
            # Convert to Dataframe
            results_secret = results[secret]
            results_secret_df = pd.DataFrame(results_secret).T

            # Save to CSV
            file_name = ut_.update_filename_with_suffix(outputcsv_filename_prefix, f"secret={secret}")
            results_secret_df.to_csv(file_name, index=True)

        return results

    
    def plot_risk_results(self, results_df, plot_title=''):
        """This function plots the batch results of the risk analysis for comparison. 
    
        Params: 
            results_df : pandas.DataFrame
                A DataFrame with the per-column (naive_value, control_value, main_value, R) values of the risk analysis. 
            plot_title : string
                A title for the graph. 
                
        Returns:
            fig_scatter : matplotlib.figure.Figure
                The figure containing the boxplot.
            ax_scatter : matplotlib.axes.Axes
                The axes on which the boxplot is shown.
        """
        xticks = ['naive_value', 'control_value', 'main_value', 'R']
        plot_data = results_df[xticks]
        fig, ax = vp.boxplot_scatter(plot_data, xticks=xticks, title=plot_title)

        return fig, ax
    
    def plot_inference_risk_results(self, inf_results, res_col='R', plot_title='Inference Evaluator (R)'):

        """
        This function creates a boxplot of the inferred risk of each secret column.

        Params: 
            inf_results : dict
                A dict containing the secret columns and associated inferred risk. 
            res_col : str
                The column specifying the results to be plotted. Default: 'R'. Options include 'R', 'main_value', 'naive_value', 'control_value'
            plot_title : str, optional 
                The title of the plot. Default: 'Inference Evaluator (R)'.

        Returns:
            fig_scatter : matplotlib.figure.Figure
                The figure containing the boxplot.
            ax_scatter : matplotlib.axes.Axes
                The axes on which the boxplot is shown.
        """

        risk_df = pd.DataFrame()
        for secret in inf_results.keys():
            results_secret_df = pd.DataFrame(inf_results[secret]).T
            risk_df[secret] = results_secret_df[res_col]
        
        xticks = risk_df.columns.to_list()
        plot_data = risk_df
        fig, ax = vp.boxplot_scatter(plot_data, xticks=xticks, title=plot_title)

        return fig, ax
