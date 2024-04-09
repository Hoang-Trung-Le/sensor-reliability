import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd



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


def plot_stacked_area_chart(data, indexes, colors, minute_locator):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), sharex="none")

    # for i, ax in enumerate(axs):
    key = list(data.keys())[0]
    print(key)
    print(data)
    value = data[key]
    # x = value.index
    y = value.values
    ax.stackplot(indexes, *y.T, labels=value.columns, colors=colors)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.tick_params(axis="x", rotation=0)
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=minute_locator))
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.margins(0, 0)
    # if i != len(axs) - 1:
    #     ax.spines["left"].set_visible(False)
    # else:
    #     ax.set_ylabel("Y Axis Label")
    ax.set_title("")
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

    return fig, ax


def plot_gantt_chart(data, task_assign_col, colors, minute_locator):
    """
    Plot a Gantt chart based on the provided data.

    Args:
        data (DataFrame): The data containing the sensor reliability information.
                
        task_assign_col (str): The name of the column in the data that contains the task assignments.
        colors (dict): A dictionary mapping each task to a color for visualization.
        minute_locator (int): The interval in minutes at which to display the x-axis ticks.
    
    Returns:
        fig, ax: The figure and axis objects for the plot.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the Gantt chart
    for i in range(len(data)):
        start = data.index[i]
        end = data.index[i + 1] if i < len(data) - 1 else data.index[-1]
        # One of the tasks in the Gantt chart
        task = data[task_assign_col][i]
        ax.barh(
            task,
            end - start,
            left=start,
            height=0.3,
            color=colors[task],
        )

    # Convert the time index to string format
    time_labels = data.index.strftime("%H:%M")

    # Set the x ticks and labels
    ax.set_xticks(data.index)
    ax.set_xticklabels(time_labels)
    ax.xaxis.set_major_locator(
        mdates.HourLocator(interval=minute_locator)
    )  # Set interval as desired

    # Rotate the x tick labels for better visibility
    # plt.xticks(rotation=0)

    # Set the x-axis label
    # ax.set_xlabel("Duration")

    # Set the y-axis label
    # ax.set_ylabel("Sensors")

    # Set the title
    # ax.set_title("Principle sensor selection mechanism based on highest reliability")

    return fig, ax
