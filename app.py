import numpy as np
import pandas as pd
from config import *
from voltage_data import *
from DS import DempsterShafer
from process_data import DataProcessor
import datetime
import os


# Clear the terminal
os.system("cls" if os.name == "nt" else "clear")


# feature_matrix_H = np.array(
#     [
#         [313.5, 559.6, 378.6, 557.4, 152.9, 762.7],
#         [1850.7, 550.8, 1734.5, 597.2, 152.3, 808.2],
#         [2669.3, 546.6, 2567.4, 534.8, 152.7, 724.1],
#     ]
# )

# sampling_matrix_S = np.array(
#     [
#         [1830.6, 553.9, 1780.5, 600.2, 152.5, 780.3],
#         [1883.5, 549.9, 1702.4, 590.0, 151.9, 813.6],
#         [1854.0, 551.7, 1738.1, 595.4, 152.1, 797.5],
#         [1882.2, 555.2, 1757.3, 575.5, 152.5, 802.4],
#     ]
# )

# feature_matrix_H = np.array(
#     [
#         [50.5, 22.6, 3.6, 5.4],
#         [60.5, 23.1, 3.3, 5.2],
#         [50.1, 35.2, 3.7, 5.5],
#         [50.2, 22.5, 6.5, 5.5],
#         [50.3, 22.8, 3.5, 8.5]
#     ]
# )

# sampling_matrix_S = np.array(
#     [
#         [60.6, 22.7, 3.9, 5.3],
#         [62.9, 23.0, 3.4, 5.3],
#         [58.4, 22.4, 3.4, 5.6],
#         [61.8, 22.9, 3.8, 5.1],
#     ]
# )

# feature_matrix_H = np.array(
#     [
#         [69.905, 18, 3.6, 5.4],
#         [85,     18, 3.3, 5.2],
#         [17,     60, 3.7, 5.5],
#         [70,     18, 40,   60],
#         [70,     18, 80,  210]
#     ]
# )

# sampling_matrix_S = np.array(
#     [
#         [45, 33, 3.36, 4.54],
#         [16, 57, 2.86, 3.19],
#         [16, 55, 2.53, 3.30],
#         [15, 62, 2.92, 3.63],
#         [ 8, 65, 2.73, 3.29]
#     ]
# )

# feature_matrix_H = np.array(
#     [
#         [69.905, 18, 3.6, 5.4],
#         [85, 18, 3.3, 5.2],
#         [17, 60, 3.7, 5.5],
#         [70, 18, 40, 60],
#         [70, 18, 80, 210],
#     ]
# )

# sampling_matrix_S = np.array(
#     [
#         [45, 33, 3.36, 4.54],
#         [16, 57, 2.86, 3.19],
#         [16, 55, 2.53, 3.30],
#         [15, 62, 2.92, 3.63],
#         [8, 65, 2.73, 3.29],
#     ]
# )

# reliability = DempsterShafer(sampling_matrix_S, feature_matrix_H)
# print("Reliability: ", reliability.result())

# params_map = {
#     "humidity": "HUMID",
#     "temperature": "TEMP",
#     "pm2.5": "PM2.5",
#     "pm10.0": "PM10",
# }


data_processor = DataProcessor(csv_file_dir, csv_file_pattern, selected_headers)
csv_data = data_processor.process_files(start=1, end=5)

time_header = selected_headers[0]
start_time_feat = "2024/02/24T04:48:42z"
end_time_feat = "2024/02/24T04:54:42z"

# print(csv_data['20231213_UTS1.csv'])
feat_mat_PA = csv_data["20240224_UTS1.csv"]

# measurement_pa1 = csv_data["20231213_UTS1.csv"]
# measurement_pa2 = csv_data["20231213_UTS2.csv"]
# measurement_pa3 = csv_data["20231213_UTS3.csv"]
# measurement_pa4 = csv_data["20231213_UTS4.csv"]
# feat_mat_voltage_normal = [
#     feat_mat_voltage[0],  # 3.3V
#     feat_mat_voltage[1],  # 3.8V
#     feat_mat_voltage[2],  # 4.0V
# ]

measurement_pa = {}
print(csv_data)
for i in range(len(normal_sensors)):
    sensor_order = normal_sensors[i]
    # filename = f"20240224_UTS{sensor_order}.csv"
    filename = csv_file_pattern.format(sensor_order)
    measurement_pa[f"sensor{sensor_order}"] = csv_data[filename]
    measurement_pa_n = measurement_pa[f"sensor{sensor_order}"]
    feat_mat_voltage_normal = measurement_pa_n[
        (measurement_pa_n[time_header] > start_time_feat)
        & (measurement_pa_n[time_header] < end_time_feat)
    ]
print(feat_mat_voltage_normal)
feat_mat_voltage = np.vstack(
    [
        np.array(voltage_data_4_0_sensor2["data"])[-1, 1:],
        np.array(voltage_data_4_0_sensor3["data"])[-1, 1:],
        np.array(voltage_data_4_0_sensor4["data"])[-1, 1:],
        np.array(voltage_data_4_0_sensor1["data"])[-7, 1:],
        # feat_mat_PA.head(5).values[:, 1:],
        # [],  # 3.3V
        # [],  # 3.8V
        # [],  # 4.0V
        # [],  # 4.2V
    ]
)
# feat_mat_voltage = np.round(feat_mat_voltage, 3)

print("Feature matrix: ", feat_mat_voltage)
print("Feature matrix shape: ", feat_mat_voltage.shape)

# sampling = csv_data["20240224_UTS1.csv"].values[:, 1:]
# print(sampling)

# # Filter the dataframe

# start_time_samp = "2024/02/24T11:54:46z"
# end_time_samp = "2024/02/24T12:44:47z"
# samp_mat = sampling[
#     (sampling[time_header] >= start_time_samp)
#     & (sampling[time_header] <= end_time_samp)
# ]

# print(samp_mat)

# Data preparation
sampling = np.array(voltage_data_4_0_sensor1["data"])[:, 1:]
print("Sampling: ", sampling)
print("Sampling shape: ", sampling.shape)

feat_mat_voltage = np.array(
    [
        [3.07000000e01, 9.36333333e01, 1.83933333e00, 2.44000000e00, 4.25333333e00],
        [3.51724138e01, 9.11551724e01, 2.96086207e00, 3.13103448e00, 8.36982759e00],
        [3.32954545e01, 9.30000000e01, 9.25250000e00, 6.45454545e00, 1.60165909e01],
        [3.10000000e01, 9.40000000e01, 1.26980000e00, 1.62000000e00, 9.36260000e00],
        [3.17166667e01, 9.37666667e01, 2.10500000e-01, 2.61000000e00, 4.30133333e00],
        [3.42333333e01, 9.35333333e01, 9.16666667e-02, 9.60000000e-01, 2.04900000e00],
    ]
)

sampling = np.array(
    [
        [3.80e01, 9.10e01, 1.70e-01, 9.00e-01, 1.34e00],
        # [3.80e01, 9.15e01, 4.50e-02, 1.00e00, 2.03e00],
        # [3.80e01, 9.15e01, 0.00e00, 8.00e-01, 8.45e-01],
    ]
)
hypotheses = [
    "Probability of normal operation",
    "Probability of input voltage fault (3.5V)",
    "Probability of input voltage fault (3.8V)",
    "Probability of input voltage fault (4.0V)",
    "Probability of input voltage fault (4.2V)",
    "Probability of input voltage fault (4.5V)",
    "Probability of uncertain faults",
]
# Execute Dempster-Shafer algorithm for each sampling matrix
for i, num_samplings in enumerate(num_samplings_vect):
    last_rows = sampling[-num_samplings:]
    print("Last rows: ", last_rows)
    print("AA:", type(last_rows), last_rows.shape)
    dst = DempsterShafer(last_rows, feat_mat_voltage)
    print(hypotheses)
    dst.hypothesis_order(hypotheses)
    reliability = dst.result()
    print(
        f"Reliability for sampling matrix {i+1} with {num_samplings} samplings: {reliability}"
    )
