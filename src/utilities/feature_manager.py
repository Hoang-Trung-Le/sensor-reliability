import os
import numpy as np
import pandas as pd
from datetime import datetime
from utilities.data_process.process_dict import mirror_and_populate_dict
from utilities.data_process.time_functions import convert_to_unix
from utilities.data_process.csv_formatter import CSVDataFormatter


class FeatureMatrixManager:
    def __init__(self, hypotheses_info):
        self.hypotheses_info = hypotheses_info
        self.temp_features_matrix_dict = {}
        self.features_matrix_dict = {}
        self.features_matrix_np = []

    def input_feature_vector(self, hypothesis_name, feature_vector):
        self.temp_features_matrix_dict[hypothesis_name] = feature_vector

    # Process test hypotheses surveyed time range

    def read_data_between_dates(self, sensors, start_date, end_date, output_folder):
        # Initialize an empty dictionary to store data frames for each sensor
        data_frames = {sensor: pd.DataFrame() for sensor in sensors}
        # print("Output folder", output_folder)
        # Iterate over each date in the specified range
        start_datetime = datetime.strptime(start_date, "%d-%m-%Y %H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%d-%m-%Y %H:%M:%S")
        dates = pd.date_range(start=start_datetime, end=end_datetime, freq="D")

        for date in dates:
            # Format the file name pattern with the date and sensors
            process_day = date.strftime("%Y%m%d")
            file_name = process_day + "_UT{}"   +  ".csv"
            data_folder = output_folder.format(process_day)
            # Iterate over each sensor and read its corresponding CSV file
            for sensor in sensors:
                file_path = os.path.join(data_folder, file_name.format(sensor))
                # print("File path:", file_path)
                if os.path.exists(file_path):
                    # print("Reading file:", file_path)
                    # Read the CSV file and append its data to the corresponding sensor DataFrame
                    df = pd.read_csv(file_path)
                    data_frames[sensor] = pd.concat(
                        [data_frames[sensor], df], ignore_index=True
                    )
                else:
                    print("File does not exist:", file_path)
        # print("Data Frames:", data_frames)
        return data_frames

    def feature_matrix_hypothesis(self, data, parameters, start_time, end_time):
        """
        This function creates a feature matrix for faulty sensors
        """
        time_header = "time_stamp"
        # print("Feature Matrix Hypothesis", start_time, end_time)
        # print("Start Time", start_time)
        # print("End Time", end_time)
        operation_data = {}
        for key, value in data.items():
            operation_data[key] = value[parameters][
                (value[time_header] > convert_to_unix(start_time))
                & (value[time_header] < convert_to_unix(end_time))
            ]
        # print(operation_data)
        # Filter out rows with zero elements
        for key, value in operation_data.items():
            operation_data[key] = value[(value != 0).all(axis=1)]

        if len(operation_data) == 1:
            key, value = next(iter(operation_data.items()))
            feat_mat_fault = value.mean(axis=0).to_numpy()
        else:
            mean_operation_data = {
                key: value.mean(axis=0) for key, value in operation_data.items()
            }
            # Calculate the mean of the means
            mean_values = [value.to_numpy() for value in mean_operation_data.values()]
            feat_mat_fault = np.mean(mean_values, axis=0)

        return feat_mat_fault

    def process_hypothesis(
        self, sensors, start_time, end_time, output_folder, parameters
    ):
        data = self.read_data_between_dates(
            sensors, start_time, end_time, output_folder
        )
        # print("Finished step 1")
        feat_mat_hypo = self.feature_matrix_hypothesis(
            data, parameters, start_time, end_time
        )
        return feat_mat_hypo

    def process_hypotheses(self, hypotheses_names, output_folder, parameters):
        for hypothesis in hypotheses_names:
            if hypothesis in list(self.hypotheses_info.keys()):
                # print("hypothesis", hypothesis)
                feat_mat_hypothesis = []
                # Get the averaged characteristic feature vector for each sampling
                for sampling in self.hypotheses_info[hypothesis]:
                    # print("sampling", sampling)
                    # for sensors, time_range in sampling:
                    sensors = sampling[0]
                    time_range = sampling[1]
                    start_time, end_time = time_range
                    feat_mat_hypothesis = self.process_hypothesis(
                        sensors, start_time, end_time, output_folder, parameters
                    )

                # Get the averaged characteristic feature vector for each hypothesis
                # Do something with feat_mat_fault
                self.input_feature_vector(hypothesis, feat_mat_hypothesis)

    # Final output of class

    def get_features_matrix_dict(self):
        return self.features_matrix_dict

    def get_features_matrix(self):
        """Get the concatenated features matrix

        Returns:
            ndarray: Returns the concatenated features matrix
        """
        if self.temp_features_matrix_dict:
            self.features_matrix_dict = mirror_and_populate_dict(
                self.hypotheses_info, self.temp_features_matrix_dict
            )
            print("Features Matrix Dict", self.features_matrix_dict)
            self.features_matrix_np = np.vstack(
                [v for v in self.features_matrix_dict.values() if v is not None]
            )
        return self.features_matrix_np
