from copy import deepcopy
import pandas as pd
import os 
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d

from mz import utils_ as ut_

class MarginalDist:
    """
    """

    def __init__(self,
        debug=False
    ):
        
        self.debug = debug
        self.marginal_dist = None
        self.fitted_marginal_dist = None
        self.sample_size = 1000
        self.params = {
            "loc": 0,
            "scale": 1,
            "a": 1,
            "b": 1,
            "c": 1,
            "ecdf": {},
            "gaussian_kde": {}
        }

        self.sample_cdf = None #cdf of samples used to fit the distribution
        self.sample_pdf = None #pdf of samples used to fit the distribution
        self.samples = None # x-values (samples) generated based on parameters (fitted or given)
        self.cdf = None # cumulative probability of new data input based on parameters (either fitted or given)
        self.pdf = None # probability of new data input based on parameters (either fitted or given)
        self.ppf = None # x-value of cumulative probability of new data input

    def load_params(self, new_params={"loc": 0, "scale": 1}):

        # Load parameters
        params = self.params

        # Replace params with specified parameters from inputs
        for param in self.params.keys():
            if param in new_params:
                if new_params[param] is not None:
                    params[param] = new_params[param]

        return params
    
    
    def beta_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None, "a":None, "b":None}, sample_size=None):
        """Compute Beta Distribution related operations"""
        self.marginal_dist = "beta"

        if (operation=="fit"):

            a, b, loc, scale = stats.beta.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.params['a'] = a
            self.params['b'] = b
            self.fitted_marginal_dist = "beta"
            self.sample_size = sample_size

            self.sample_pdf = stats.beta.pdf(data, a=self.params['a'], b=self.params['b'], loc=self.params['loc'], scale=self.params['scale'])
            self.sample_cdf = stats.beta.cdf(data, a=self.params['a'], b=self.params['b'], loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):

            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size

            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")
            
            self.samples = stats.beta.rvs(a=params['a'], b=params['b'], loc=params['loc'], scale=params['scale'], size=size)

            return self.samples

        elif (operation=="pdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = stats.beta.pdf(data, a=params['a'], b=params['b'], loc=params['loc'], scale=params['scale'])

            return self.pdf

        elif (operation=="cdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.beta.cdf(data, a=params['a'], b=params['b'], loc=params['loc'], scale=params['scale'])

            return self.cdf

        elif (operation=="ppf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.beta.ppf(data, a=params['a'], b=params['b'], loc=params['loc'], scale=params['scale'])

            return self.ppf

    def empirical_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None, "a":None}, sample_size=None):

        self.marginal_dist = "emp"

        if (operation=="fit"):

            self.fitted_marginal_dist = "emp"

            # Build U from sample data
            self.sample_cdf = self.ecdf(data)

            # Sort
            sorting_index = np.argsort(data)
            sorted_data = np.take(data, sorting_index, 0)
            sorted_u = np.take(self.sample_cdf, sorting_index, 0)

            # Pad
            init_val = 0
            x1 = np.r_[-np.inf, sorted_data]
            u1 = np.r_[init_val, sorted_u]

            # Store sorted x, u as parameters to eCDF
            self.params["ecdf"] = {
                "x": x1,
                "u": u1
            }
            self.sample_size = sample_size

        elif (operation=="sample"):
            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size
            x = params["ecdf"]["x"]
            u = params["ecdf"]["u"]

            interp_fn = self.inv_CDF_fn(x,u)

            uni = MarginalDist()
            uni.uni_dist(operation="sample", new_params={"loc":0, "scale":1}, sample_size=size)
            self.samples = interp_fn(uni.samples)

            return self.samples

        elif (operation=="cdf"):

            params = self.load_params(new_params=new_params)
            x = params["ecdf"]["x"]
            u = params["ecdf"]["u"]

            self.cdf = self.eCDF_fn(data, x=x, u=u)

            return self.cdf
        
        elif (operation=="ppf"):

            params = self.load_params(new_params=new_params)
            x = params["ecdf"]["x"]
            u = params["ecdf"]["u"]

            interp_fn = self.inv_CDF_fn(x,u)
            self.ppf = interp_fn(data)
            
            return self.ppf
            
    def laplace_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None}, sample_size=None):
        """Compute Laplace Distribution related operations"""

        self.marginal_dist = "laplace"

        if (operation=="fit"):
            loc, scale = stats.t.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.fitted_marginal_dist = "laplace"
            self.sample_size = sample_size

            self.sample_cdf = stats.laplace.cdf(data, loc=self.params['loc'], scale=self.params['scale'])
            self.sample_pdf = stats.laplace.pdf(data, loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):
            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size

            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")

            self.samples = stats.laplace.rvs(loc=params['loc'], scale=params['scale'], size=size)

            return self.samples
        
        elif (operation=="pdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = stats.laplace.pdf(data, loc=params['loc'], scale=params['scale'])

            return self.pdf
        
        elif (operation=="cdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.laplace.cdf(data, loc=params['loc'], scale=params['scale'])

            return self.cdf
        
        elif (operation=="ppf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.laplace.ppf(data, loc=params['loc'], scale=params['scale'])

            return self.ppf
        
    def loglaplace_dist(self, data=None, operation="fit", new_params={"c": None, "loc":None, "scale":None}, sample_size=None):
        """Compute log Laplace Distribution related operations"""

        self.marginal_dist = "loglaplace"

        if (operation=="fit"):

            c, loc, scale = stats.loglaplace.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.params['c'] = c
            self.fitted_marginal_dist = "loglaplace"
            self.sample_size = sample_size

            self.sample_pdf = stats.loglaplace.pdf(data, c=self.params['c'], loc=self.params['loc'], scale=self.params['scale'])
            self.sample_cdf = stats.loglaplace.cdf(data, c=self.params['c'], loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):

            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size

            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")

            self.samples = stats.loglaplace.rvs(c=params['c'], loc=params['loc'], scale=params['scale'], size=size)

            return self.samples
        
        elif (operation=="pdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")
            
            self.pdf = stats.loglaplace.pdf(data, c=params['c'], loc=params['loc'], scale=params['scale'])

            return self.pdf
        
        elif (operation=="cdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.loglaplace.cdf(data, c=params['c'], loc=params['loc'], scale=params['scale'])

            return self.cdf
        
        elif (operation=="ppf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.loglaplace.ppf(data, c=params['c'], loc=params['loc'], scale=params['scale'])

            return self.ppf


    def gamma_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None, "a":None}, sample_size=None):
        """Compute Beta Distribution related operations"""

        self.marginal_dist = "gamma"

        if (operation=="fit"):

            a, loc, scale = stats.gamma.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.params['a'] = a
            self.fitted_marginal_dist = "gamma"
            self.sample_size = sample_size

            self.sample_pdf = stats.gamma.pdf(data, a=self.params['a'], loc=self.params['loc'], scale=self.params['scale'])
            self.sample_cdf = stats.gamma.cdf(data, a=self.params['a'], loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):

            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size

            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")

            self.samples = stats.gamma.rvs(a=params['a'], loc=params['loc'], scale=params['scale'], size=size)

            return self.samples

        elif (operation=="pdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")
            
            self.pdf = stats.gamma.pdf(data, a=params['a'], loc=params['loc'], scale=params['scale'])

            return self.pdf

        elif (operation=="cdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.gamma.cdf(data, a=params['a'], loc=params['loc'], scale=params['scale'])

            return self.cdf

        elif (operation=="ppf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.gamma.ppf(data, a=params['a'], loc=params['loc'], scale=params['scale'])

            return self.ppf


    def gaussian_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None}, sample_size=None):
        """Compute Gaussian Distribution related operations"""

        self.marginal_dist = "gaussian"

        if (operation=="fit"):
            
            loc, scale = stats.norm.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.fitted_marginal_dist = "gaussian"
            self.sample_size = sample_size

            self.sample_cdf = stats.norm.cdf(data, loc=self.params['loc'], scale=self.params['scale'])
            self.sample_pdf = stats.norm.pdf(data, loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):

            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size
            
            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")
                
            self.samples = stats.norm.rvs(loc=params['loc'], scale=params['scale'], size=size)

            return self.samples

        elif (operation=="pdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = stats.norm.pdf(data, loc=params['loc'], scale=params['scale'])

            return self.pdf

        elif (operation=="cdf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.norm.cdf(data, loc=params['loc'], scale=params['scale'])

            return self.cdf

        elif (operation=="ppf"):

            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.norm.ppf(data, loc=params['loc'], scale=params['scale'])

            return self.ppf
        
    def gaussian_kde_dist(self, data=None, operation="fit", new_params={"scale": None}, sample_size=None, bw_method=None, weights=None):
        """Compute Gaussian Kernel Density Estimate related operations"""

        self.marginal_dist = "gaussian_kde"

        if (operation=="fit"):
            self.params['gaussian_kde']['bw_method'] = bw_method
            self.params['gaussian_kde']['weights'] = weights
            self.fitted_marginal_dist = "gaussian_kde"
            self.sample_size = sample_size

            model = stats.gaussian_kde(data, bw_method=bw_method, weights=weights)

            self.gaussian_kde_model = model
            self.params['scale'] = model.factor
            
            self.sample_pdf = self.gaussian_kde_model.evaluate(data)

            # Expand integration bounds
            lower, upper = self._get_bounds(data)
            step = 0.01
            expanded_x = np.arange(lower, upper, step)
            expanded_u = self.generic_cdf(expanded_x, self.gaussian_kde_model.evaluate)
            self.params["gaussian_kde"] = {
                "x": expanded_x,
                "u": expanded_u
            }

            interp_fn = self.fwd_CDF_fn(expanded_x, expanded_u)
            self.sample_cdf = interp_fn(data)


        if (operation=="pdf"):
            params = self.params #does not accept new_params

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = self.gaussian_kde_model.evaluate(data)

            return self.pdf

        if (operation=="cdf"):
            params = self.params #does not accept new_params

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            # y_cdf = np.array([tup[0] for tup in [quad(norm.pdf, a, b) for a, b in [(a, b) for a, b in zip(x, x[1:len(x)])]]] + [0]).cumsum()

            x = params["gaussian_kde"]["x"]
            u = params["gaussian_kde"]["u"]

            interp_fn = self.fwd_CDF_fn(x=x, u=u)
            self.cdf = interp_fn(data)

            return self.cdf
        
        if (operation=="ppf"):
            params = self.params #does not accept new_params

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            # x = self.params['x']
            # lower, upper = self._get_bounds(x)
            # step = 0.01
            # expanded_x = np.arange(lower, upper, step)
            # expanded_u = self.generic_cdf(expanded_x, self.gaussian_kde_model.evaluate)

            # interp_fn = self.inv_CDF_fn(expanded_x, expanded_u)
            # self.ppf = interp_fn(data)

            x = params["gaussian_kde"]["x"]
            u = params["gaussian_kde"]["u"]

            interp_fn = self.inv_CDF_fn(x, u)
            self.ppf = interp_fn(data)

            return self.ppf, u, x


    def t_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None}, sample_size=None):
        """Compute Student t Distribution related operations"""

        self.marginal_dist = "student_t"

        if (operation=="fit"):
            loc, scale = stats.t.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.fitted_marginal_dist = "student_t"
            self.sample_size = sample_size

            self.sample_cdf = stats.t.cdf(data, loc=self.params['loc'], scale=self.params['scale'])
            self.sample_pdf = stats.t.pdf(data, loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):

            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size

            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")

            self.samples = stats.t.rvs(loc=params['loc'], scale=params['scale'], size=size)

            return self.samples
        
        elif (operation=="pdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = stats.t.pdf(data, loc=params['loc'], scale=params['scale'])

            return self.pdf
        
        elif (operation=="cdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.t.cdf(data, loc=params['loc'], scale=params['scale'])

            return self.cdf
        
        elif (operation=="ppf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.t.ppf(data, loc=params['loc'], scale=params['scale'])

            return self.ppf
        

    def uni_dist(self, data=None, operation="fit", new_params={"loc":None, "scale":None}, sample_size=None):
        """Compute Uniform Distribution related operations"""

        self.marginal_dist = "uniform"

        if (operation=="fit"):
            loc, scale = stats.uniform.fit(data)
            self.params['loc'] = loc
            self.params['scale'] = scale
            self.fitted_marginal_dist = "uniform"
            self.sample_size = sample_size

            self.sample_cdf = stats.uniform.cdf(data, loc=self.params['loc'], scale=self.params['scale'])
            self.sample_pdf = stats.uniform.pdf(data, loc=self.params['loc'], scale=self.params['scale'])

        elif (operation=="sample"):
            params = self.load_params(new_params=new_params)
            if (sample_size is not None):
                self.sample_size = sample_size
            size = self.sample_size
            
            if (self.debug):
                print(f"Parameters used for sampling:/n {params}")
                
            self.samples = stats.uniform.rvs(loc=params['loc'], scale=params['scale'], size=size)

            return self.samples

        elif (operation=="pdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PDF:/n {params}")

            self.pdf = stats.uniform.pdf(data, loc=params['loc'], scale=params['scale'])

            return self.pdf

        elif (operation=="cdf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating CDF:/n {params}")

            self.cdf = stats.uniform.cdf(data, loc=params['loc'], scale=params['scale'])

            return self.cdf

        elif (operation=="ppf"):
            params = self.load_params(new_params=new_params)

            if (self.debug):
                print(f"Parameters used for generating PPF:/n {params}")

            self.ppf = stats.uniform.ppf(data, loc=params['loc'], scale=params['scale'])

            return self.ppf
        
    
    
    # HELPER FUNCTIONS
    def ecdf(self, x):
        """
        This function computes the empirical cumulative distribution function (ECDF) of a given array x. Use only for continuous distributions.
            (a) first sort the array x, creating two new arrays xs and ys, such that 
                - xs is a sorted version of x;
                - ys is the corresponding probability that a value is less than or equal to the x value.
            (b) create a sorting index which is used to map the sorted array xs to the unsorted array x. 
            (c) use the sorting index to map the ys array to the y array which can then be used to evaluate the ECDF.
        """

        xs = np.sort(x)
        ys = np.arange(1, len(xs)+1) / float(len(xs))

        sorting_index = np.argsort(x)
        inverse = np.empty_like(sorting_index)
        inverse[sorting_index] = np.arange(sorting_index.size)

        y = ys[inverse]

        return y
    
    # Build eCDF step function
    def eCDF_fn(self, input, x, u, init_val=0):
        """
        This function is an implementation of an empirical cumulative distribution function (eCDF), using fitted parameters. It finds the best position of each element in the input array in the x-array, determines the corresponding cumulative probability from the u-array, and interpolates the cumulative probability for each element in the input array.
        Inputs:
            input: array
            x: array of x values
            u: array of corresponding cumulative probability values
            init_val: optional, initial value for the cumulative probability array
        Output:
            interp
        """
        
        # x1 = np.r_[-np.inf, x] #moved to "fit" operation in empirical dist
        # u1 = np.r_[init_val, u]
        x1 = x
        u1 = u

        input_pos = np.searchsorted(x1, input, 'left') - 1
        interp = u1[input_pos]

        return interp
    
    # Build CDF forward function
    def fwd_CDF_fn(self, x, u):

        a = np.argsort(u)
        fn = interp1d(x[a], u[a], kind='linear', fill_value='extrapolate')

        return fn
    
    # Build CDF inverse function
    def inv_CDF_fn(self, x, u):

        a = np.argsort(u)
        fn = interp1d(u[a], x[a], kind='linear', fill_value='extrapolate')

        return fn
    
    # Generic CDF using integration
    def generic_cdf(self, x, fn_pdf):
        from scipy.integrate import quad

        expanded_x = x

        cdf_list = []
        for i in range(len(expanded_x)-1):
            a = expanded_x[i]
            b = expanded_x[i+1]
            cdf_list.append(quad(fn_pdf, a, b)[0])
        cdf_list.append(0)

        return np.cumsum(cdf_list)
    
    # Generic PDF by differentiating CDF
    def generic_pdf(self, x, fn_cdf):
        from scipy.misc import derivative

        # derivative is facing deprecation (find another)
    
    # Expand the bounds of dataset
    def _get_bounds(self, X):
        lower = np.min(X) - (5 * np.std(X))
        upper = np.max(X) + (5 * np.std(X))

        return lower, upper
    