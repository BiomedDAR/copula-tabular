# This example demonstrates the use of the MarginalDist class to generate synthetic data for a univariate dataset.

# LOAD DEPENDENCIES
import pprint, sys, os
import matplotlib.pyplot as plt
import numpy as np

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)

from mz.MarginalDist import MarginalDist
from scipy import stats

# BUILD PLOT AREA
fig, (ax1, ax2) = plt.subplots(1,2)

# GENERATE A "FICTIONAL" DATA SAMPLE USING SCIPY
# In this example, we use the scipy stats package to generate a fictitious multimodal sample, based on a Gaussian and a gamma distribution.
samples_1 = stats.gamma.rvs(a=4, loc=2, scale=5, size=400)
samples_2 = stats.norm.rvs(loc=60, scale=6, size=400)
samples = np.concatenate((samples_1, samples_2))

# VISUALISE THEORETICAL PDF, CDF AND HISTOGRAM OF GENERATED DATA
# Plot Histogram of Data Sample
ax1.hist(samples, density=True, bins='auto', alpha=0.8, color='blue', label=f'Histogram of Original Samples n={(len(samples))}')

# INITIALISE A MARGINALDIST CLASS
univariate = MarginalDist(debug=True)

# LEARN THE OPTIMAL DISTRIBUTION FROM THE DATA SAMPLES
univariate.fit(data=samples)
print(f"optimum univariate: {univariate.fitted_marginal_dist}")

# PLOT THE LEARNED PDF, CDF, AND HISTOGRAM OF SYNTHETIC SAMPLES
# Plot Learned CDF
x = np.linspace(np.min(samples), np.max(samples), 100)
learned_cdf = univariate.cdf_wrapper(data=x)
ax2.plot(x, learned_cdf, 'k-', lw=1, label='Fitted CDF using learned parameters')

# Plot Learned PDF
x = np.linspace(np.min(samples), np.max(samples), 100)
learned_pdf = univariate.pdf_wrapper(data=x)
ax1.plot(x, learned_pdf, 'k-', lw=1, label='Fitted PDF using learned parameters')

# Create a synthetic sample from learned parameters
x = stats.uniform.rvs(size=5000)
learned_ppf = univariate.ppf_wrapper(data=x)
ax1.hist(learned_ppf, density=True, bins='auto', alpha=0.8, color='gray', label=f"Histogram of Synthetic Samples n={len(learned_ppf)}")

# PLOT STUFF
ax1.legend(loc='best', frameon=False)
ax2.legend(loc='best', frameon=False)
plt.show()