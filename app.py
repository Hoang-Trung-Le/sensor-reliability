import numpy as np

from DS import DempsterShafer


feature_matrix_H = np.array(
    [
        [313.5, 559.6, 378.6, 557.4, 152.9, 762.7],
        [1850.7, 550.8, 1734.5, 597.2, 152.3, 808.2],
        [2669.3, 546.6, 2567.4, 534.8, 152.7, 724.1],
    ]
)

sampling_matrix_S = np.array(
    [
        [1830.6, 553.9, 1780.5, 600.2, 152.5, 780.3],
        [1883.5, 549.9, 1702.4, 590.0, 151.9, 813.6],
        [1854.0, 551.7, 1738.1, 595.4, 152.1, 797.5],
        [1882.2, 555.2, 1757.3, 575.5, 152.5, 802.4],
    ]
)

reliability = DempsterShafer()
print(reliability.result(sampling_matrix_S, feature_matrix_H))
