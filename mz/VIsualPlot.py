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
        position (tuple, int): Position of the axis on the figure
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
    if isinstance(position, tuple):
        ax = ax or fig.add_subplot(position[0], position[1], position[2])
    else:
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

        # position_tuple = int(str(no_rows) + str(no_cols) + str(index+1))
        position_tuple = (int(no_rows), int(no_cols), int(index+1))

        if (index == 0):
            (ax_hist_out, fig_histogram) = hist(x_real, position = position_tuple, label=f"Original: n = {len(x_real)}")
            ax_hist.append(ax_hist_out)
            (ax_hist[index], fig_histogram) = hist(x_syn, ax=ax_hist[index], fig=fig_histogram, color='grey', title=f'Histogram Plot for {var}', label=f"Synthetic: n={len(x_syn)}")
        else:
            (ax_hist_out, fig_histogram) = hist(x_real, fig=fig_histogram, position = position_tuple, label=f"Original: n = {len(x_real)}")
            ax_hist.append(ax_hist_out)
            (ax_hist[index], fig_histogram) = hist(x_syn, ax=ax_hist[index], fig=fig_histogram, color='grey', title=f'Histogram Plot for {var}', label=f"Synthetic: n={len(x_syn)}")

    return ax_hist, fig_histogram


def corrMatrix(data, fig=None, position=None, title=None, x_label_rot=None):
    """Build single correlation matrix of data.
    
    Params:
        data (pd.DataFrame): Data as a pandas dataframe
        fig (matplotlib Figure): existing figure to add plot to (optional)
        position (3-tuple, int): subplot position (optional)
        title (str): title of plot (optional)
        x_label_rot (float or {'vertical', 'horizontal'}): rotation of x-labels. Default is 'vertical'
    Returns:
        ax (matplotlib Axis): axis for the plot
        fig (matplotlib Figure): figure with the plot
    """

    fig = fig or plt.figure()
    position = position or 111
    x_label_rot = x_label_rot or 'vertical'
    if isinstance(position, tuple):
        ax = fig.add_subplot(position[0], position[1], position[2])
    else:
        ax = fig.add_subplot(position)

    # BUILD CORRELATION
    corr = data.corr()
    np_corr = corr.to_numpy()

    im = ax.matshow(np_corr, interpolation='nearest', cmap='jet', vmin=-1, vmax=1)

    ax.set_title(title, fontsize=8)
    ax.set_xticklabels(['']+list(corr.columns), rotation=x_label_rot)
    ax.set_yticklabels(['']+list(corr.columns))

    for (i, j), z in np.ndenumerate(np_corr):
        ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

    fig.colorbar(im, ax=ax)

    return ax, fig

def corrMatrix_compare(real_data, syn_data, options={}):

    if "x_label_rot" in options:
        x_label_rot = options["x_label_rot"]
    else:
        x_label_rot = None

    fig_corr = plt.figure()

    ax_corr_1, fig_corr = corrMatrix(real_data, fig=fig_corr, position=121, title='Plot of Correlation Matrix (REAL)', x_label_rot=x_label_rot)
    ax_corr_2, fig_corr = corrMatrix(syn_data, fig=fig_corr, position=122, title='Plot of Correlation Matrix (SYN)', x_label_rot=x_label_rot)

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
        position : 3-tuple or 3-digit int, optional
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
    if isinstance(position, tuple):
        ax = ax or fig.add_subplot(position[0], position[1], position[2])
    else:
        ax = ax or fig.add_subplot(position)

    ax.scatter(x_data, y_data, s=8, color=color, marker=marker, label=label)
    ax.legend()
    ax.set_title(title)

    return ax, fig

def scatterPlot_multiple(data_df, n_plot_cols=2, ref=None, color='blue', marker='.'):
    """This function creates a scatterplot of data_df[ref] vs. other columns in data_df, with optional formatting as provided.

    Params: 
        data_df : dataframe
            The x,y-values of data to be plotted.
        n_plot_cols : int, optional
            The number of columns in the fig. Default: 2
        ref : str, optional
            The reference column (x-data). Every other column will be plotted against it. 
            Default: None (if None, then first column will be taken as reference).
            Option: 'autopermute': N choose 2, exhaustive plot
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

    listOfVar = list(data_df.columns)

    if ref is None:
        ref_out = listOfVar[0]
    elif ref == 'autopermute':
        ref_out = list(itertools.combinations(listOfVar, 2))
    else:
        ref_out = str(ref)

    if ref == 'autopermute':
        n = len(ref_out)
        print(n)
        en = ref_out
    else:
        n = len(data_df.columns)
        en = listOfVar

    n_plot_cols = int(n_plot_cols)
    n_plot_rows = math.ceil(n/n_plot_cols)

    axes_h = []
    for index, var in enumerate(en):
        if ref == 'autopermute':
            x_data = data_df[var[0]]
            y_data = data_df[var[1]]
            plt_title = f'Plot of {var[1]} against {var[0]}'
        else:
            x_data = data_df[ref_out]
            y_data = data_df[var]
            plt_title = f'Plot of {var} against {ref_out}'

        position_tuple = (int(n_plot_rows), int(n_plot_cols), int(index+1))

        if (index==0):
            fig = None

        (axes_out, fig) = scatterPlot(x_data, y_data, title=plt_title, position=position_tuple, fig=fig, color=color, marker=marker)

        axes_h.append(axes_out)

    fig.tight_layout()
    return axes_h, fig

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

def scatterPlot_multiple_compare(data_df, syn_data_df, n_plot_cols=2, ref=None):
    """This function creates a superposition of two scatterplots:
     1: scatterplot of data_df[ref] vs. other columns in data_df;
     2: scatterplot of syn_data_df[ref] vs. other columns in syn_data_df;
     with optional formatting as provided.

    Params: 
        data_df : dataframe
            The x,y-values of data to be plotted.
        syn_data_df : dataframe
            The x-y-values of synthetic data to be plotted.
        n_plot_cols : int, optional
            The number of columns in the fig. Default: 2
        ref : str, optional
            The reference column (x-data). Every other column will be plotted against it. 
            Default: None (if None, then first column will be taken as reference).
            Option: 'autopermute': N choose 2, exhaustive plot

    Returns:
        ax : matplotlib.axes.Axes
            The axes on which the data was plotted.
        fig : matplotlib.figure.Figure
            The figure on which the data was plotted.
    
    """

    listOfVar = list(data_df.columns)

    if ref is None:
        ref_out = listOfVar[0]
    elif ref == 'autopermute':
        ref_out = list(itertools.combinations(listOfVar, 2))
    else:
        ref_out = str(ref)

    if ref == 'autopermute':
        n = len(ref_out)
        print(n)
        en = ref_out
    else:
        n = len(data_df.columns)
        en = listOfVar

    n_plot_cols = int(n_plot_cols)
    n_plot_rows = math.ceil(n/n_plot_cols)

    axes_h = []
    # for index, var in enumerate(list(data_df.columns)):
    for index, var in enumerate(en):
        if ref == 'autopermute':
            x_data_real = data_df[var[0]]
            y_data_real = data_df[var[1]]
            x_data_syn = syn_data_df[var[0]]
            y_data_syn = syn_data_df[var[1]]
            plt_title = f'Plot of {var[1]} against {var[0]}'
        else:
            x_data_real = data_df[ref_out]
            y_data_real = data_df[var]
            x_data_syn = syn_data_df[ref_out]
            y_data_syn = syn_data_df[var]
            plt_title = f'Plot of {var} against {ref_out}'

        position_tuple = (int(n_plot_rows), int(n_plot_cols), int(index+1))

        if (index==0):
            fig = None

        (axes_out, fig) = scatterPlot(x_data_real, y_data_real, label="Real", position=position_tuple, fig=fig, color='blue', marker='.')

        (axes_out, fig) = scatterPlot(x_data_syn, y_data_syn, label="Synthetic", fig=fig, ax=axes_out, color='grey', marker='x', title=plt_title)

        axes_h.append(axes_out)

    fig.tight_layout()
    return axes_h, fig

def anony_inference_plot(results):
    """This function creates a barplot of the inferred risk of each secret column.

    Params: 
        results : array pairs
            An array of pairs containing the columns and associated inferred risk. 

    Returns:
        fig_scatter : matplotlib.figure.Figure
            The figure containing the barplot.
        ax_scatter : matplotlib.axes.Axes
            The axes on which the barplot is shown.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    risks = [res[1].risk().value for res in results]
    columns = [res[0] for res in results]

    ax.bar(x=columns, height=risks, alpha=0.5, ecolor='black', capsize=10)
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Measured Inference Risk")
    _ = ax.set_xlabel("Secret Column")

    return fig, ax

def boxplot_scatter(data, xticks, title):
    """This function creates a boxplot of the data for plotting variable values. 
    
    Params: 
        data : list of lists or pandas.DataFrame
            A list where each element is a list of values for a given variable. Used as input for plt boxplot fn.
        xticks : list
            A list of labels which will be associated with each boxplot.
        title : string
            A title for the graph. 
            
    Returns:
        fig_scatter : matplotlib.figure.Figure
            The figure containing the boxplot.
        ax_scatter : matplotlib.axes.Axes
            The axes on which the boxplot is shown.
    """

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # Creating plot
    bp = ax.boxplot(data)
    ax.set_title(title, fontsize=14, fontweight='bold')

    x_tick_rotation = 45 if len(xticks) > 6 else 'horizontal'
    x_tick_ha = 'right' if len(xticks) > 6 else 'center'
    ax.set_xticks([i+1 for i in range(len(xticks))], labels=xticks, minor=False, ha=x_tick_ha, rotation=x_tick_rotation)
    
    return fig, ax