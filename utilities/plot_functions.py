import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


def plot_stacked_area_chart(data, indexes, colors, time_locator):
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
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=time_locator))
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


def plot_gantt_chart():
    # Plot the Gantt chart
    for i in range(len(reliability_comparison)):
        start = reliability_comparison.index[i]
        end = (
            reliability_comparison.index[i + 1]
            if i < len(reliability_comparison) - 1
            else reliability_comparison.index[-1]
        )
        # print("Start:\n", start, "\nEnd:\n", end)
        chosen_sensor = reliability_comparison["Highest Reliability"][i]
        ax.barh(
            chosen_sensor,
            end - start,
            left=start,
            height=0.3,
            color=sensor_colors[chosen_sensor],
        )
    # Convert the time index to string format
    time_labels = reliability_comparison.index.strftime('%H:%M')

    # Set the x ticks and labels
    ax.set_xticks(reliability_comparison.index)
    ax.set_xticklabels(time_labels)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Set interval as desired

    # Rotate the x tick labels for better visibility
    plt.xticks(rotation=0)
    # Set the x-axis label
    ax.set_xlabel("Duration")

    # Set the y-axis label
    ax.set_ylabel("Sensors")

    # Set the title
    # ax.set_title("Principle sensor selection mechanism based on highest reliability")






