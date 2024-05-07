import pandas as pd
import numpy as np
from .time_functions import convert_to_unix
from src.config.config import *


def resample_data(
    df: pd.DataFrame,
    resample_time: str,
    method: str,
    fillna: str,
    columns: list = None,
):
    """
    This function resamples data
    """

    if columns is None:
        print("Please provide columns")
        return

    # Resample the data
    resampled_df = df[columns].resample(resample_time).agg(method)

    # Fill missing values
    resampled_df = resampled_df.fillna(fillna)

    return resampled_df


def sampling_matrix(
    df: pd.DataFrame,
    window_size: int,
    stride: int,
    columns: list = None,
):
    """
    This function creates a sampling matrix
    """

    if columns is None:
        print("Please provide columns")
        return

    # Create a sampling matrix
    sampling_matrix = np.zeros((len(df) - window_size, window_size, len(columns)))

    for i in range(len(df) - window_size):
        sampling_matrix[i] = df[columns].iloc[i : i + window_size].values

    return sampling_matrix


def feature_matrix_normal():
    """
    This function creates a feature matrix for normal sensors
    """
    pass


def feature_matrix_faulty(data, start_time, end_time):
    """
    This function creates a feature matrix for faulty sensors
    """
    fault_operation_data = {}
    for key, value in data.items():
        fault_operation_data[key] = value[parameter_headers][
            (value[time_header] > convert_to_unix(start_time))
            & (value[time_header] < convert_to_unix(end_time))
        ]
        # print(fault_operation_data)
    first_key = list(fault_operation_data.keys())[0]
    first_value = fault_operation_data[first_key]
    # print("First Value", first_value)
    average_value = first_value.mean(axis=0).to_numpy()

    feat_mat_fault = average_value
    # print("Feature Matrix Fault", feat_mat_fault)
    return feat_mat_fault
