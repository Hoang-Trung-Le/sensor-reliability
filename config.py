from datetime import datetime
import time

csv_file_dir = "data/20240224"
csv_file_pattern = "20240224_UTS{}.csv"  # Replace with the pattern for your file names
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
header_to_field_mapping = {
    "UTCDateTime": "UTCDateTime",
    "current_temp_f": "temperature",
    "current_humidity": "humidity",
    "pm1_0_atm": "pm1_0_atm",
    "pm2_5_atm": "pm2_5_atm",
    "pm10_0_atm": "pm10_0_atm",
    "pm2.5_aqi_atm": "pm2.5_aqi_atm",
    "p_0_3_um": "p_0_3_um",
    "p_0_5_um": "p_0_5_um",
    "p_1_0_um": "p_1_0_um",
    "p_2_5_um": "p_2_5_um",
    "p_5_0_um": "p_5_0_um",
    "p_10_0_um": "p_10_0_um",
}

field_list = [
    # "firmware_version",
    # "hardware",
    "humidity",
    "temperature",
    # "pressure_b",
    # "analog_input",
    # "memory",
    # "rssi",
    # "uptime",
    # "pm1.0_cf_1_a",
    # "pm2.5_cf_1_a",
    # "pm10.0_cf_1_a",
    # "pm2.5_atm_a",
    # "pm10.0_atm_a",
    # "0.3_um_count_a",
    # "0.5_um_count_a",
    # "1.0_um_count_a",
    # "2.5_um_count_a",
    # "5.0_um_count_a",
    # "10.0_um_count_a",
    # "pm1.0_cf_1_b",
    # "pm2.5_cf_1_b",
    # "pm10.0_cf_1_b",
    # "pm1.0_atm_b",
    # "pm2.5_atm_b",
    # "pm10.0_atm_b",
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

num_sensors = 4
faulty_sensor = [1]
normal_sensors = [2, 3, 4]
sensor_names = ["UTS1", "UTS2", "UTS3", "UTS4"]
sensro_codenames = ["S1", "S2", "S3", "S4"]
sensor_codes = [180263, 180261, 180259, 180257]
group_id = 1872

temp_calib = 4
humid_calib = 7

num_samplings_vect = [1]
hypotheses = [
    "Probability of normal operation like sensor 2",
    "Probability of normal operation like sensor 3",
    "Probability of normal operation like sensor 4",
    "Probability of input voltage fault (4.0V)",
    "Probability of other faults",
]

# Define the hypotheses for Dempster-Shafer with code names
hypotheses = {
    "Normal Operation": {
        "Normal Operation": "N0",
        "Normal Operation like Sensor 1": "N1",
        "Normal Operation like Sensor 2": "N2",
        "Normal Operation like Sensor 3": "N3",
        "Normal Operation like Sensor 4": "N4"
    },
    "Voltage Fault": {

        "Voltage 3.5V": "F_V3_5",
        "Voltage 3.5V": "F_V3_8",
        "Voltage 4.0V": "F_V4_0",
        "Voltage 4.0V": "F_V4_2",

    },
    "Overheating": {
        "Overheating": "F_H"
    },
    "Dust": {
        "Dust": "F_D"
    },
    "Connection": {
        "Connection": "F_Lost_Com"
    },
    "Uncertain": {
        "Uncertain": "F_X"
    }
}

# Access hypotheses by category and get their code names
normal_operation_hypotheses = hypotheses["Normal Operation"]
voltage_fault_hypotheses = hypotheses["Voltage Fault"]
overheating_hypotheses = hypotheses["Overheating"]
dust_hypotheses = hypotheses["Dust"]

# Print hypotheses and their code names for each category
print("Normal Operation Hypotheses:", normal_operation_hypotheses)
print("Voltage Fault Hypotheses:", voltage_fault_hypotheses)
print("Overheating Hypotheses:", overheating_hypotheses)
print("Dust Hypotheses:", dust_hypotheses)


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


# Define faulty scenarios
# Scenario 1: Voltage drop
voltage_drop = [3.5, 3.8, 4.0, 4.2, 4.5]
voltage_data = {
    "api_version": "V1.0.11-0.0.49",
    "time_stamp": 1709009205,
    "sensor_index": 180263,
    "start_timestamp": 1709006820,
    "end_timestamp": 1709007720,
    "average": 0,
    "fields": [
        "time_stamp",
        "humidity",
        "temperature",
        "0.3_um_count",
        "0.5_um_count",
        "1.0_um_count",
        "2.5_um_count",
        "5.0_um_count",
        "10.0_um_count",
        "pm1.0_atm",
        "pm2.5_atm",
        "pm10.0_atm",
    ],
    "data": [
        [
            1709006866,
            61.5,
            81.5,
            2523.995,
            758.94,
            117.29,
            33.19,
            18.54,
            1.4,
            27.325,
            43.0,
            68.47,
        ],
        [
            1709007043,
            58.0,
            83.5,
            612.745,
            201.075,
            33.35,
            20.12,
            12.025,
            3.42,
            7.215,
            11.73,
            27.865,
        ],
        [
            1709007163,
            56.5,
            83.5,
            1773.575,
            451.41,
            210.995,
            51.735,
            32.905,
            0.625,
            13.52,
            34.405,
            72.685,
        ],
        [
            1709007283,
            55.5,
            84.5,
            1248.31,
            354.95,
            148.185,
            43.97,
            30.87,
            0.73,
            11.555,
            24.62,
            65.445,
        ],
        [
            1709007403,
            55.0,
            84.5,
            556.83,
            158.265,
            88.755,
            35.045,
            22.56,
            0.87,
            2.74,
            13.81,
            41.39,
        ],
        [
            1709007523,
            54.5,
            84.5,
            1976.855,
            460.005,
            243.33,
            24.805,
            15.155,
            0.25,
            14.18,
            29.525,
            50.275,
        ],
        [
            1709007643,
            53.5,
            85.0,
            911.8,
            262.425,
            96.91,
            31.46,
            21.39,
            0.495,
            9.175,
            18.685,
            43.02,
        ],
    ],
}
