import pandas as pd
import matplotlib.pyplot as plt
from config import *
from DS import DempsterShafer
from process_data import DataProcessor
from datetime import datetime
import os
import time
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# from pa_get_group_data import convert_to_unix

# Clear the terminal
os.system("cls" if os.name == "nt" else "clear")

csv_file_dir = "data/20240311"
selected_headers = [
    "UTCDateTime",
    "current_temp_f",
    "current_humidity",
    "pm1_0_atm",
    "pm2_5_atm",
    "pm10_0_atm",
    "pm2.5_aqi_atm",
    "p_0_3_um",
    "p_0_5_um",
    "p_1_0_um",
    "p_2_5_um",
    "p_5_0_um",
    "p_10_0_um",
]  # Replace with the headers you want
selected_header = [
    "time_stamp",
    "group_id",
    "member_id",
    "id",
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    # "0.3_um_count",
    # "0.5_um_count",
    # "1.0_um_count",
    # "2.5_um_count",
    # "5.0_um_count",
    # "10.0_um_count",
    "date_time_utc",
]
parameter_headers = [
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    # "0.3_um_count",
    # "0.5_um_count",
    # "1.0_um_count",
    # "2.5_um_count",
    # "5.0_um_count",
    # "10.0_um_count",
]
csv_file_pattern = "20240311_UTS{}.csv"  # Replace with the pattern for your file names
data_processor = DataProcessor(csv_file_dir, csv_file_pattern, selected_header)
csv_data = data_processor.process_files(start=1, end=5)

time_header = selected_header[0]

# Define time intervals
# time_intervals = [
#     {"start": "05-03-2024 18:30:00", "end": "05-03-2024 19:03:00"},
#     {"start": "05-03-2024 19:04:00", "end": "05-03-2024 19:30:00"},
#     {"start": "05-03-2024 19:30:00", "end": "05-03-2024 20:03:00"},
#     {"start": "05-03-2024 20:03:00", "end": "05-03-2024 20:30:00"},
#     {"start": "05-03-2024 20:30:00", "end": "05-03-2024 21:00:00"},
#     {"start": "05-03-2024 21:15:00", "end": "05-03-2024 21:45:00"},
# ]
time_intervals = [
    {"start": "11-03-2024 14:00:00", "end": "11-03-2024 15:00:00"},
    {"start": "11-03-2024 15:15:00", "end": "11-03-2024 16:00:00"},
    {"start": "11-03-2024 16:10:00", "end": "11-03-2024 17:00:00"},
    {"start": "11-03-2024 17:00:00", "end": "11-03-2024 18:00:00"},
    {"start": "11-03-2024 18:00:00", "end": "11-03-2024 18:30:00"},
]
# voltage_fault_sequences = ["4.5V", "4.2V", "4.0V", "3.8V", "3.5V", "5.0V"]
voltage_fault_sequences = ["3.5V", "3.8V", "4.0V", "4.2V", "4.5V"]

# print(csv_data['20231213_UTS1.csv'])
# feat_mat_PA = csv_data["20240224_UTS1.csv"]

measurement_pa = {}

# Initialize a DataFrame to store the averages
averages_df = pd.DataFrame(columns=parameter_headers)
print("A", averages_df)
averages_list = []


def convert_to_unix(date_str, format="%d-%m-%Y %H:%M:%S"):
    """
    Convert a datetime string to a Unix timestamp using the specified format.

    Args:
        date_str (str): Datetime string.
        format (str): Format of the datetime string (default is '%d-%m-%Y %H:%M:%S').

    Returns:
        int: Unix timestamp.
    """
    try:
        formatted_time = datetime.strptime(date_str, format)
    except ValueError:
        format_no_time = "%d-%m-%Y"
        formatted_time = datetime.strptime(date_str, format_no_time)

    unix_time = int(time.mktime(formatted_time.timetuple()))
    return unix_time


for sensor_order in range(1, num_sensors + 1):
    filename = csv_file_pattern.format(sensor_order)
    measurement_pa[f"sensor{sensor_order}"] = csv_data[filename]
    measurement_pa_n = measurement_pa[f"sensor{sensor_order}"]

    for interval in time_intervals:
        start_time_feat = interval["start"]
        end_time_feat = interval["end"]
        interval_data = []

        # Extract data for the current time interval
        data_subset = measurement_pa_n[
            (measurement_pa_n[time_header] > convert_to_unix(start_time_feat))
            & (measurement_pa_n[time_header] < convert_to_unix(end_time_feat))
        ]
        print("Data subset ", sensor_order)
        print(data_subset)

        # Calculate average for each data type
        parameter_avgs = {}
        for parameter in parameter_headers:
            parameter_avgs[parameter] = data_subset[parameter].mean()
            print("Parameter avgs: ", parameter_avgs)
        # Store the mean values in a new row of averages_list
        averages_list.append(parameter_avgs)

averages_df = pd.DataFrame(averages_list)
print("Averages: ", averages_df)
# Draw parallel coordinate plot

# Specify the class column separately
class_column = pd.DataFrame({"Sensor": ["S1", "S2", "S3", "S4"]})

# Create a list to store the plot_data for each fault sequence
plot_data_list = []

# Iterate over the voltage_fault_sequences
for i in range(len(voltage_fault_sequences)):
    # Calculate the indices for the current fault sequence
    indices = [j + i for j in range(0, len(averages_df), len(voltage_fault_sequences))]
    # Select the corresponding rows from averages_df
    plot_data = averages_df.iloc[indices]
    # Reset index of plot_data before concatenating
    plot_data.reset_index(drop=True, inplace=True)
    # Concatenate class_column with plot_data
    plot_data = pd.concat([plot_data, class_column], axis=1)
    # Append plot_data to the list
    plot_data_list.append(plot_data)

print("\nPlot data: ", plot_data_list)

average_fault_df = pd.DataFrame(columns=averages_df.columns)
for plot_data in plot_data_list:
    fault_name = plot_data.iloc[0]["Sensor"]
    plot_data = plot_data.iloc[0].drop("Sensor")
    plot_data.name = fault_name
    average_fault_df.loc[len(average_fault_df)] = plot_data

average_fault_df = average_fault_df.reset_index()
average_fault_df = average_fault_df.rename(columns={"index": "Fault"})
average_fault_df = average_fault_df.set_index("Fault")
# Convert dataframe to numpy array
average_fault_array = average_fault_df.to_numpy()
# Save dataframe to Excel file
average_fault_df.to_csv("average_fault_data.csv", index=True)

print("Average fault dataframe:\n", average_fault_df)
print("Average fault array:\n", average_fault_array)

# Iterate over the plot_data_list and plot parallel coordinate plots
# Create the "fig" directory if it doesn't exist
if not os.path.exists("fig"):
    os.makedirs("fig")
# Define a custom colormap
custom_colormap = LinearSegmentedColormap.from_list(
    "custom_colormap",
    [(0, "red"), (0.3, "green"), (0.6, "orange"), (1, "blue")],
)
plot_large_fontsize = 18
plot_medium_fontsize = 16
for i, plot_data in enumerate(plot_data_list):
    plt.figure(figsize=(10, 6))  # Optional: adjust figure size
    pd.plotting.parallel_coordinates(
        plot_data,
        class_column="Sensor",
        cols=["pm1.0_atm", "pm2.5_alt", "pm10.0_atm"],
        use_columns=False,
        colormap=custom_colormap,
        axvlines=True,
        linewidth=3,  # Set the line width for all lines
    )  # 'A' is the column to use for color
    plt.legend(fontsize=plot_large_fontsize)  # Increase the font size of the legend

    # Add axis labels
    # Modify the display names of the parameters in the horizontal axis
    # plt.xticks(["A","B","C"])
    plt.xticks(
        range(3), ["PM1.0", "PM2.5", "PM10.0"], fontsize=plot_medium_fontsize
    )  # Custom xtick names and font size
    plt.xlabel(
        "Parameter", fontsize=plot_large_fontsize
    )  # Set x-axis label and font size
    plt.ylabel(
        "Concentration (µg/m³)", fontsize=plot_large_fontsize
    )  # Set y-axis label and font size
    plt.title(
        f"Input voltage {voltage_fault_sequences[i]}",
        fontweight="bold",
        fontsize=plot_large_fontsize,
    )  # Set plot title, font weight, and font size

    # Save the plot as a PNG file
    # plt.savefig(f"fig/{voltage_fault_sequences[i]}.png")

    # plt.show()
