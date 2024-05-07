from datetime import datetime
import pandas as pd
import seaborn as sns
import time

csv_file_dir = "data/20240224"
csv_file_pattern = "20240224_UTS{}.csv"  # Replace with the pattern for your file names
selected_headers = [
    "time_stamp",
    "group_id",
    "member_id",
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    # "scattering_coefficient",
    # "deciviews",
    # "visual_range", 
    "date_time_utc",
]
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

csv_headers = [
    "time_stamp",
    "group_id",
    "member_id",
    "id",
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    "date_time_utc",
]

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
    # "scattering_coefficient",
    # "deciviews",
    # "visual_range", 
]

retrieve_parameters = [
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    "scattering_coefficient",
    "deciviews",
    "visual_range", 
]

parameter_headers = [
    "humidity",
    "temperature",
    "pm1.0_atm",
    "pm2.5_alt",
    "pm10.0_atm",
    # "scattering_coefficient",
    # "deciviews",
    # "visual_range", 
]

time_header = csv_headers[0]

num_sensors = 4
faulty_sensor = [1]
normal_sensors = [2, 3, 4]
sensor_names = ["UTS1", "UTS2", "UTS3", "UTS4"]
sensro_codenames = ["S1", "S2", "S3", "S4"]
sensor_codes = [180263, 180261, 180259, 180257]
group_id = 1872

sensors_data = {
    "id": [180263, 180261, 180259, 180257],
    "codename": ["S1", "S2", "S3", "S4"],
    "name": ["UTS1", "UTS2", "UTS3", "UTS4"],
    "group_id": [1872, 1872, 1872, 1872],
    "status": ["faulty", "normal", "normal", "normal"],
}

sensors_data_df = pd.DataFrame(sensors_data)

temp_calib = 4
humid_calib = 7

num_samplings_vect = [1]

# Define the hypotheses for Dempster-Shafer with code names
hypotheses = {
    "Normal": {
        "Normal operation": "N0",
        "Normal as Sensor 1": "N1",
        "Normal as Sensor 2": "N2",
        "Normal as Sensor 3": "N3",
        "Normal as Sensor 4": "N4",
    },
    "Voltage": {
        "Voltage 3.5V": "F_V3_5",
        "Voltage 3.8V": "F_V3_8",
        "Voltage 4.0V": "F_V4_0",
        "Voltage 4.2V": "F_V4_2",
    },
    "Overheat": "F_H",
    "Aerosol": "F_A",
    "Compound": {
        "Overheat and Voltage 3.5V": "F_H_V3_5",
        "Overheat and Voltage 3.8V": "F_H_V3_8",
        # "Overheat and Voltage 4.0V": "F_H_V4_0",
        # "Overheat and Voltage 4.2V": "F_H_V4_2",
        "Aerosol and Voltage 3.5V": "F_D_V3_5",
        "Aerosol and Voltage 3.8V": "F_D_V3_8",
        # "Aerosol and Voltage 4.0V": "F_D_V4_0",
        # "Aerosol and Voltage 4.2V": "F_D_V4_2",
        # Add other combinations as needed
    },
    "Communication": "F_Com",
    "Uncertain": "F_X",
}

# Define color palettes for each category
color_palettes = {
    "Normal": sns.color_palette("Greens_r", n_colors=len(hypotheses["Normal"])),
    "Voltage": sns.color_palette("Oranges_r", n_colors=len(hypotheses["Voltage"])),
    "Overheat": ["red"],
    "Aerosol": ["blue"],
    "Compound": sns.color_palette("Purples", n_colors=len(hypotheses["Compound"])),
    "Communication": ["black"],
    "Uncertain": ["lightgray"],
}

hypotheses_colors = {}
for category, cases in hypotheses.items():
    if isinstance(cases, dict):
        # If subcases is a dictionary, assign colors to each subcase
        for subcase, code in cases.items():
            hypotheses_colors[subcase] = color_palettes[category].pop(0)
    else:
        # If subcases is a single hypothesis, assign color directly
        hypotheses_colors[category] = color_palettes[category][0]
