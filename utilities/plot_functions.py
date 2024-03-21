import matplotlib.pyplot as plt
import pandas as pd


# def plot_line_graph():


def plot_line_graph_df(
    df: pd.DataFrame,
    x_column=None,
    y_columns=None,
    title=None,
    xlabel=None,
    ylabel=None,
    color: str = None,
    # linestyle: str,
    # marker: str,
    figsize: tuple = None,
):
    """
    This function plots a graph from a dataframe
    """

    if y_columns is None:
        print("Please provide x and y columns")
        return

    fig, ax = plt.subplots(figsize=figsize)

    # Use Dataframe index if x_column is not provided
    x = df.index if x_column is None else df[x_column]

    for i, y_column in enumerate(y_columns):
        plt.plot(
            x,
            df[y_column],
            label=y_column,
            color=color[i],
        )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax
