import pandas as pd
import numpy as np
from scipy import stats
import itertools
import math

try:
    import matplotlib.pyplot as plt
except RuntimeError as e:
    if 'Python is not installed as a framework.' in e.message:
        import matplotlib
        matplotlib.use('PS')   # Avoid crash on macos
        import matplotlib.pyplot as plt



def hist(data_1d, fig=None, ax=None, position=None, title=None, alpha=0.8, color='blue', label=''):
    """Function to generate a histogram plot.

    Parameters:
        data_1d (array-like): 1 dimensional numerical data
        fig (matplotlib figure): Matplotlib figure to plot
        ax (axis object): Axis object on the figure
        position (int): Position of the axis on the figure
        title (string): Chart title
        alpha (float): Opacity for the chart
        color (string): Color of the histogram bars
        label (string): Label for the histogram

    Returns:
        ax (axis object): Axis object on the figure
        fig (matplotlib figure): Matplotlib figure to plot
    """

    fig = fig or plt.figure()
    position = position or 111
    ax = ax or fig.add_subplot(position)

    data_dropped_na = data_1d.dropna()

    ax.hist(data_dropped_na, density=True, bins='auto', alpha=alpha, color=color, label=label)

    ax.legend(loc='best', frameon=False)
    ax.set_title(title, fontsize=8)

    return ax, fig

def hist_compare(real_data, syn_data, var_list, no_cols=2):

    no_rows = len(var_list) // no_cols + math.ceil(len(var_list) % no_cols)
    ax_hist = []
    for index, var in enumerate(var_list):
        x_real = real_data[var]
        x_syn = syn_data[var]

        position_tuple = int(str(no_rows) + str(no_cols) + str(index+1))

        if (index == 0):
            (ax_hist_out, fig_histogram) = hist(x_real, position = position_tuple, label=f"Original: n = {len(x_real)}")
            ax_hist.append(ax_hist_out)
            (ax_hist[index], fig_histogram) = hist(x_syn, ax=ax_hist[index], fig=fig_histogram, color='grey', title=f'Histogram Plot for {var}', label=f"Synthetic: n={len(x_syn)}")
        else:
            (ax_hist_out, fig_histogram) = hist(x_real, fig=fig_histogram, position = position_tuple, label=f"Original: n = {len(x_real)}")
            ax_hist.append(ax_hist_out)
            (ax_hist[index], fig_histogram) = hist(x_syn, ax=ax_hist[index], fig=fig_histogram, color='grey', title=f'Histogram Plot for {var}', label=f"Synthetic: n={len(x_syn)}")

    return ax_hist, fig_histogram


def corrMatrix(data, fig=None, position=None, title=None):
    """Build single correlation matrix of data.
    
    Params:
        data (pd.DataFrame): Data as a pandas dataframe
        fig (matplotlib Figure): existing figure to add plot to (optional)
        position (int): subplot position (optional)
        title (str): title of plot (optional)

    Returns:
        ax (matplotlib Axis): axis for the plot
        fig (matplotlib Figure): figure with the plot
    """

    fig = fig or plt.figure()
    position = position or 111
    ax = fig.add_subplot(position)

    # BUILD CORRELATION
    corr = data.corr()
    np_corr = corr.to_numpy()

    im = ax.matshow(np_corr, interpolation='nearest', cmap='jet', vmin=-1, vmax=1)

    ax.set_title(title, fontsize=8)
    ax.set_xticklabels(['']+list(corr.columns))
    ax.set_yticklabels(['']+list(corr.columns))

    for (i, j), z in np.ndenumerate(np_corr):
        ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

    fig.colorbar(im, ax=ax)

    return ax, fig

def corrMatrix_compare(real_data, syn_data):
    fig_corr = plt.figure()

    ax_corr_1, fig_corr = corrMatrix(real_data, fig=fig_corr, position=121, title='Plot of Correlation Matrix (REAL)')
    ax_corr_2, fig_corr = corrMatrix(syn_data, fig=fig_corr, position=122, title='Plot of Correlation Matrix (SYN)')

    return ax_corr_1, ax_corr_2, fig_corr


def scatterPlot(x_data, y_data, label='', fig=None, ax=None, position=None, title=None, color='blue', marker='.',):
    """This function creates a scatterplot of x_data vs. y_data, with optional formatting and labeling as provided.
    
    Params: 
        x_data : array_like
            The x-values of data to be plotted.
        y_data : array_like
            The y-values of the data to be plotted.
        label : str, optional
            The label for the data. Default: ''.
        fig : matplotlib.figure.Figure, optional
            The figure on which the data should be plotted. Default: None.
        ax : matplotlib.axes.Axes, optional
            The axes on which the data should be plotted. Default: None.
        position : int or 3-digit int, optional
            The position of the subplot in the figure. Default: None.
        title : str, optional
            The title for the subplot. Default: None.
        color : str, optional
            The color of the plotted points. Default: 'blue'.
        marker : str, optional
            The marker style to be used for the points. Default: '.'.

    Returns:
        ax : matplotlib.axes.Axes
            The axes on which the data was plotted.
        fig : matplotlib.figure.Figure
            The figure on which the data was plotted.
    """

    fig = fig or plt.figure()
    position = position or 111
    ax = ax or fig.add_subplot(position)

    ax.scatter(x_data, y_data, s=8, color=color, marker=marker, label=label)
    ax.legend()
    ax.set_title(title)

    return ax, fig

def scatterPlot_compare(real_data, syn_data, x_var, y_var, fig=None):
    """This function creates a scatterplot of x_var vs. y_var for both real and synthetic data.

    Params: 
        real_data : pandas.DataFrame
            The dataframe containing the real data.
        syn_data : pandas.DataFrame
            The dataframe containing the synthetic data.
        x_var : str
            The variable to plot on the x-axis.
        y_var : str
            The variable to plot on the y-axis.
        fig : matplotlib.figure.Figure, optional
            The figure on which the data should be plotted. Default: None.

    Returns:
        fig_scatter : matplotlib.figure.Figure
            The figure containing the scatterplot.
        ax_scatter : matplotlib.axes.Axes
            The axes on which the scatterplot is shown.
    """

    fig_scatter = fig or plt.figure()

    x_real = real_data[x_var]
    y_real = real_data[y_var]

    x_syn = syn_data[x_var]
    y_syn = syn_data[y_var]

    ax_scatter, fig_scatter = scatterPlot(x_real, y_real, label="Real", fig=fig_scatter, color='blue', marker='.')
    
    ax_scatter, fig_scatter = scatterPlot(x_syn, y_syn, label="Synthetic", fig=fig_scatter, ax=ax_scatter, color='grey', marker='x', title=f"Scatterplot of {y_var} against {x_var}")

    return fig_scatter, ax_scatter