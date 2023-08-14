from mz.MarginalDist import MarginalDist
from mz import utils_ as ut_
import pandas as pd
import numpy as np
from scipy import stats

EPSILON = np.finfo(np.float32).eps

class GaussianCopula:
    """

    Change Log: (MZ): 13-07-2023: Added print_copula_params()
    (MZ): 14-07-2023: Added conditions for self.fitted boolean in self.fit()
    """

    def __init__(self,
        debug=False,
        correlation_method="kendall"
    ):
        
        self.debug = debug
        self.var_names = None #array of column names found in data dataframe
        self.univariates = None #dict of MarginalDist class
        self.correlation= None #correlation matrix
        self.correlation_method = correlation_method #method for computing correlation
        self.fitted = False
    
    def print_copula_params(self):

        print('Displaying Copula Parameters:')
        for var_name in self.var_names:
            var_univariate = self.univariates[var_name]
            print(f"Learned marginal distribution for {var_name}: {var_univariate.fitted_marginal_dist}")

    def compute_correlation(self, data, method='kendall', transform_to_normal=False):
        """Compute the (pairwise) correlation matrix using input data
        method (str): options available: 'kendall' (default)
        """

        if (self.debug):
            print(f"Correlation Fitting Method={method}")

        # TRANSFORM TO NORMAL
        if (transform_to_normal):
            temp_dict = {}
            for var_name, var in data.items():
                univariate = self.univariates[var_name]
                temp_U = univariate.cdf_wrapper(data=var)
                norm_var = stats.norm.ppf(temp_U)
                temp_dict[var_name] = norm_var
            norm_data_df = pd.DataFrame.from_dict(temp_dict)
            data_df = norm_data_df
        else:
            data_df = data

        if (method=='kendall'):
            corr_matrix_df = data_df.corr(method='kendall') #data_df is DataFrame
            corr_matrix_np = np.nan_to_num(corr_matrix_df.to_numpy(), nan=0.0)
            corr_matrix_np = np.sin(corr_matrix_np * np.pi/2)
        elif (method=='spearman'):
            corr_matrix_df = data_df.corr(method='spearman') #data_df is DataFrame
            corr_matrix_np = np.nan_to_num(corr_matrix_df.to_numpy(), nan=0.0)
            corr_matrix_np = np.sin(corr_matrix_np * np.pi/6) * 2
        elif (method=='pearson'):
            corr_matrix_df = data_df.corr(method='pearson') #data_df is DataFrame
            corr_matrix_np = np.nan_to_num(corr_matrix_df.to_numpy(), nan=0.0)

        # If correlation matrix is not positive definite, make it so
        corr_matrix_np = ut_.makePD(corr_matrix_np)
        corr_matrix_df = pd.DataFrame(corr_matrix_np, index=self.var_names, columns=self.var_names)

        return corr_matrix_df


    def fit(self, data, marginal_dist_dict=None):
        """Compute the distribution for each variable and then its covariance matrix
        """

        var_names = []
        univariates = {}
        if marginal_dist_dict is None:
            marginal_dist_dict = {}

        self.fitted = True

        for var_name, var in data.items():

            # Initialise MarginalDist
            if (self.debug):
                print(f"Fitting var: {var_name}")
            univariate = MarginalDist(debug=self.debug)

            # Get candidates for Marginal Distributions
            if var_name in marginal_dist_dict:
                candidates = marginal_dist_dict[var_name]
            else:
                candidates = None

            # Fit univariate using MarginalDist
            fit_success = univariate.fit(data=var, candidates=candidates)
            if (not fit_success):
                self.fitted = False

            # Update array
            var_names.append(var_name)
            univariates[var_name] = univariate

        self.var_names = var_names
        self.univariates = univariates

        # Compute correlation matrix
        if (self.correlation is None):
            self.correlation = self.compute_correlation(data, method=self.correlation_method)

        

    def conditional_Gaussian(self, conditions):
        """Compute the parameters (mean, covariance) of a conditional multivariate normal distribution.
        Takes in a pd.series variable: conditions"""

        columns2 = conditions.index
        columns1 = self.correlation.columns.difference(columns2)

        sigma11 = self.correlation.loc[columns1, columns1].to_numpy()
        sigma12 = self.correlation.loc[columns1, columns2].to_numpy()
        sigma21 = self.correlation.loc[columns2, columns1].to_numpy()
        sigma22 = self.correlation.loc[columns2, columns2].to_numpy()

        mu1 = np.zeros(len(columns1))
        mu2 = np.zeros(len(columns2))

        sigma12sigma22inv = sigma12 @ np.linalg.inv(sigma22)

        mu_bar = mu1 + sigma12sigma22inv @ (conditions - mu2)
        sigma_bar = sigma11 - sigma12sigma22inv @ sigma21

        return mu_bar, sigma_bar, columns1

    def sample(self, size=1, conditions=None):
        """
            conditions (dict)
        """

        # check fit
        if not self.fitted:
            raise Error('Model must be fitted before sampling.')
        
        # Generate a multivariate random number vector (X_1, \dots, X_m) in an arbitrary domain following the Gaussian joint distribution \Phi(0,P) [P=correlation matrix]
        if conditions is None:
            # means = np.zero(len(self.var_names))
            means = None
            correlation_matrix = self.correlation
            sampled_var_names = self.var_names
        else: # generate conditional Gaussian distribution
            norm_conv_dict={}
            for var_name in conditions: # convert to normal distribution using marginal probability integral transform
                
                if var_name in self.var_names:
                    univariate = self.univariates[var_name]
                    temp_U = univariate.cdf_wrapper(data=conditions[var_name]).clip(EPSILON, 1-EPSILON)
                    norm_conv_dict[var_name] = stats.norm.ppf(temp_U)
            conditions_norm_pdseries = pd.Series(norm_conv_dict)
            means, correlation_matrix, sampled_var_names = self.conditional_Gaussian(conditions_norm_pdseries)


        norm_samples_np = stats.multivariate_normal.rvs(mean=means, cov=correlation_matrix, size=size)
        if (size==1):
            norm_samples_np = norm_samples_np.reshape(1,-1)
        norm_samples_df = pd.DataFrame(norm_samples_np, columns=sampled_var_names)

        # Transform (X_1, \dots, X_m) to (U_1, \dots, U_m) \in [0,1] where U_j = \phi(X_j) [\phi is the standard Gaussian distribution]
        # Compute synthetic data D_j = F^{-1}_j(U_j)
        output = {}
        for var_name in self.var_names:
            univariate = self.univariates[var_name]
            if conditions is None:
                U_j = stats.norm.cdf(norm_samples_df[var_name])
                output[var_name] = univariate.ppf_wrapper(data=U_j)
            else:
                if var_name in conditions:
                    output[var_name] = np.full(size, conditions[var_name])
                else:
                    U_j = stats.norm.cdf(norm_samples_df[var_name])
                    output[var_name] = univariate.ppf_wrapper(data=U_j)

        syn_samples_df = pd.DataFrame(data=output)


        return syn_samples_df



class Error(Exception):
    """Base class for other exceptions"""
    pass