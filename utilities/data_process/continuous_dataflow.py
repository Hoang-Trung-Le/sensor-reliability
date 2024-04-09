import pandas as pd
import numpy as np


def continuous_dataflow(
    sensor_data: pd.DataFrame,
    normal_prob: pd.DataFrame,
    measurement_columns,
    sensor_assignment_column: str,
    dict_sensor_name_to_key,
):
    """
    This function creates a continuous dataflow from a dataframe
    """

    # Preallocate the continuous dataframe
    time_index = normal_prob.index
    cont_data = pd.DataFrame(
        index=time_index, columns=measurement_columns, dtype=np.float64
    )

    for timestamp in time_index:
        sensor = normal_prob.loc[timestamp, sensor_assignment_column]
        print("Sensor: ", sensor)
        sensor_data_row = sensor_data[dict_sensor_name_to_key[sensor]].loc[timestamp]
        print(sensor_data_row)
        
        cont_data.loc[timestamp, measurement_columns] = sensor_data_row[
            measurement_columns
        ].values

    return cont_data
