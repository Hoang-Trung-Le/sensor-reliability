import pandas as pd
import os


class CSVDataFormatter:
    def __init__(self, csv_file_dir, csv_file_pattern, selected_headers):
        self.csv_file_dir = csv_file_dir
        self.csv_file_pattern = csv_file_pattern
        self.selected_headers = selected_headers

    def select_columns(self, csv_file):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Select the desired columns
        selected_df = df[self.selected_headers]

        return selected_df

    def csv_to_df(self, start, end):
        file_data = {}  # Dictionary to store the result_df of each file

        for i in range(start, end):
            csv_file = self.csv_file_pattern.format(i)
            # print(csv_file)
            csv_file_path = os.path.join(self.csv_file_dir, csv_file)
            print(csv_file_path)
            result_df = self.select_columns(csv_file_path)

            # Display the resulting DataFrame
            # print(result_df)
            csv_file_name = csv_file.split(".")[0]
            file_data[csv_file_name] = result_df  # Save result_df into the dictionary

        # print(csv_file_path)
        return file_data  # Return the dictionary containing the result_df of each file
