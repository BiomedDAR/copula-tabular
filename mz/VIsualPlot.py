import pandas as pd
import numpy as np
from scipy import stats
import itertools

try:
    import matplotlib.pyplot as plt
except RuntimeError as e:
    if 'Python is not installed as a framework.' in e.message:
        import matplotlib
        matplotlib.use('PS')   # Avoid crash on macos
        import matplotlib.pyplot as plt



def hist(data_1d, fig=None, ax=None, position=None, title=None, alpha=0.8, color='blue', label=''):

    fig = fig or plt.figure()
    position = position or 111
    ax = ax or fig.add_subplot(position)

    ax.hist(data_1d, density=True, bins='auto', alpha=alpha, color=color, label=label)

    ax.legend(loc='best', frameon=False)
    ax.set_title(title, fontsize=8)

    return ax, fig

def corrMatrix(data, fig=None, position=None, title=None):
    """Build single correlation matrix of data
    Args:
        data (pd.DataFrame)
    """

    fig = fig or plt.figure()
    position = position or 111
    ax = fig.add_subplot(position)

    # BUILD CORRELATION
    corr = data.corr()
    np_corr = corr.to_numpy()

    im = ax.matshow(np_corr, interpolation='nearest', cmap='jet')

    ax.set_title(title, fontsize=8)
    ax.set_xticklabels(['']+list(corr.columns))
    ax.set_yticklabels(['']+list(corr.columns))

    for (i, j), z in np.ndenumerate(np_corr):
        ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

    fig.colorbar(im, ax=ax)

    return ax, fig

def scatterPlot(x_data, y_data, label='', fig=None, ax=None, position=None, title=None, color='blue', marker='.',):

    fig = fig or plt.figure()
    position = position or 111
    ax = ax or fig.add_subplot(position)

    ax.scatter(x_data, y_data, s=8, color=color, marker=marker, label=label)
    ax.legend()
    ax.set_title(title)

    return ax, fig