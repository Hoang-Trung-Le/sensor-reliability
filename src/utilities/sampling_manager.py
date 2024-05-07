import os
import numpy as np
import pandas as pd
from datetime import datetime
from utilities.data_process.time_functions import convert_to_unix


class SamplingMatrixManager:
    def __init__(self, sampling_info):
        self.sampling_info = sampling_info
        self.sampling_matrix = []  # pd.DataFrame()
        self.time_indexes = []

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
            file_name = process_day + "_UT{}" + ".csv"
            data_folder = output_folder.format(process_day)
            # Iterate over each sensor and read its corresponding CSV file
            for sensor in sensors:
                file_path = os.path.join(data_folder, file_name.format(sensor))
                print("File path:", file_path)
                if os.path.exists(file_path):
                    print("Reading file:", file_path)
                    # Read the CSV file and append its data to the corresponding sensor DataFrame
                    df = pd.read_csv(
                        file_path,
                        parse_dates=["date_time_utc"],
                        index_col="date_time_utc",
                    )
                    # print("Data Frame before concat", df)
                    data_frames[sensor] = pd.concat(
                        [data_frames[sensor], df], ignore_index=False
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
        operation_data = {}
        for key, value in data.items():
            operation_data[key] = value[parameters][
                
                    (value[time_header] >= convert_to_unix(start_time))
                    & (value[time_header] < convert_to_unix(end_time))
                
            ]
        # print("Op", operation_data)
        self.time_indexes = {sensor: df.index for sensor, df in operation_data.items()}
        # print("Time Indexes", self.time_indexes)
        return operation_data
        

    def process_hypothesis(
        self, sensors, start_time, end_time, output_folder, parameters
    ):
        data = self.read_data_between_dates(
            sensors, start_time, end_time, output_folder
        )
        # print("Finished step 1")
        self.sampling_matrix = self.feature_matrix_hypothesis(
            data, parameters, start_time, end_time
        )
        # return feat_mat_hypo

    def process_hypotheses(self, output_folder, parameters):
        # for hypothesis in hypotheses_names:
        #     if hypothesis in list(self.hypotheses_info.keys()):
        #         # print("hypothesis", hypothesis)
        #         feat_mat_hypothesis = []
        #         # Get the averaged characteristic feature vector for each sampling
        #         for sampling in self.hypotheses_info[hypothesis]:
        #             # print("sampling", sampling)
        #             # for sensors, time_range in sampling:
        #             sensors = sampling[0]
        #             time_range = sampling[1]
        #             start_time, end_time = time_range
        # for sampling in self.sampling_info:
        sensors = self.sampling_info[0]
        start_time, end_time = self.sampling_info[1]
        print("Sensors1", sensors)
        print("Start Time", start_time)
        print("End Time", end_time)
        self.process_hypothesis(
            sensors, start_time, end_time, output_folder, parameters
        )

        # Get the averaged characteristic feature vector for each hypothesis
        # Do something with feat_mat_fault
        # self.input_feature_vector(hypothesis, feat_mat_hypothesis)

    # Final output of class

    def get_sampling_matrix(self):
        return self.sampling_matrix

    def get_sampling_indexes(self):
        return self.time_indexes

    # def get_features_matrix_dict(self):
    #     return self.features_matrix_dict

    # def get_features_matrix(self):
    #     """Get the concatenated features matrix

    #     Returns:
    #         ndarray: Returns the concatenated features matrix
    #     """
    #     if self.temp_features_matrix_dict:
    #         self.features_matrix_dict = mirror_and_populate_dict(
    #             self.hypotheses_info, self.temp_features_matrix_dict
    #         )
    #         print("Features Matrix Dict", self.features_matrix_dict)
    #         self.features_matrix_np = np.vstack(
    #             [v for v in self.features_matrix_dict.values() if v is not None]
    #         )
    #     return self.features_matrix_np
