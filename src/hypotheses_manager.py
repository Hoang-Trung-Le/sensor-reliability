from utilities.data_process.process_dict import mirror_and_populate_dict


class HypothesesManager:
    def __init__(self, hypothesis_list):
        self.hypotheses = {}
        self.hypotheses["original"] = hypothesis_list
        self.hypotheses["codes"] = {}
        for key, value in hypothesis_list.items():
            if isinstance(value, dict):
                self.hypotheses["codes"].update(value)
            else:
                self.hypotheses["codes"][key] = value

        print(self.hypotheses["codes"])
        print("HypothesesManager: ", self.hypotheses)
        self.hypotheses_data = {}
        self.test_hypotheses = []

    # def add_hypothesis(self, hypothesis):
    #     self.hypotheses.append(hypothesis)

    # def get_hypotheses(self):
    #     return self.hypotheses

    # def get_hypothesis(self, index):
    #     return self.hypotheses[index]

    # def get_hypothesis_by_name(self, name):
    #     for hypothesis in self.hypotheses:
    #         if hypothesis.name == name:
    #             return hypothesis
    #     return None

    # def remove_hypothesis(self, index):
    #     del self.hypotheses[index]

    # def remove_hypothesis_by_name(self, name):
    #     for i, hypothesis in enumerate(self.hypotheses):
    #         if hypothesis.name == name:
    #             del self.hypotheses[i]
    #             return

    def populate_info(self, info_name, data):
        self.hypotheses_data[info_name] = data
        self.hypotheses[info_name] = mirror_and_populate_dict(
            self.hypotheses["codes"], data
        )
        print(f"populate {info_name}", self.hypotheses[info_name])

    def activation(self, trigger):
        # Check if the trigger is in hypotheses and is not None
        self.filter_hypotheses(trigger)
        self.test_hypotheses = list(self.hypotheses_data[trigger].keys())
        for key, value in list(self.hypotheses.items()):
            if key != trigger:
                self.filter_hypotheses_by_features(key, self.hypotheses[trigger])

    def filter_hypotheses(self, trigger):
        if trigger in self.hypotheses and self.hypotheses[trigger] is not None:
            print(f"Filtering hypotheses for the trigger: {trigger}")
            hypotheses_copy = self.hypotheses[trigger].copy()
            for key, value in list(hypotheses_copy.items()):
                if value is not None:
                    # Filter out None values in the triggered hypothesis
                    if isinstance(value, dict):
                        # Make a copy of the value dictionary
                        value_copy = value.copy()
                        for k, v in list(value_copy.items()):
                            if v is None:
                                self.hypotheses[trigger][key].pop(k)
                else:
                    # Handle the case where value is None
                    self.hypotheses[trigger].pop(key)
        else:
            print(f"No active hypothesis for the trigger: {trigger}")

    def filter_hypotheses_by_features(self, feature, filtered_hypotheses):
        """
        Filter other dictionaries based on the keys and subkeys of the filtered one.
        """
        hypotheses_copy = self.hypotheses[feature].copy()
        # print("hypotheses_copy", hypotheses_copy)
        for key, value in list(hypotheses_copy.items()):
            if key in filtered_hypotheses:
                # print("key", key)
                # print("feature", feature)
                if isinstance(value, dict):
                    # Make a copy of the value dictionary
                    value_copy = value.copy()
                    for k, v in list(value_copy.items()):
                        if k not in filtered_hypotheses[key]:
                            # print("k", k)
                            self.hypotheses[feature][key].pop(k)
            else:
                # Include the key if it's not a dictionary
                self.hypotheses[feature].pop(key)
        # self.hypotheses[key] = filtered_hypotheses

    def get_hypotheses_info(self, feature):
        return self.hypotheses[feature]

    def extract_values(self, feature):
        """
        Extract all the values from the dictionary.
        """
        main_keys = self.test_hypotheses
        # print("main_keys", main_keys)
        values = []
        for key, value in self.hypotheses[feature].items():
            # print("key", key)
            if key in main_keys:
                # print("Key in main keys", key, main_keys)
                values.append(value)
            else:
                if isinstance(value, dict):
                    values.extend(value.values())
        return values

    def extract_keys(self, feature):
        """
        Extract keys if their value isn't a dictionary and subkeys if the value of the key is a dictionary.
        """
        keys = []
        for key, value in self.hypotheses[feature].items():
            if isinstance(value, dict):
                keys.extend(value.keys())
            else:
                keys.append(key)
        return keys

    def get_test_hypotheses(self):
        return self.test_hypotheses

    def get_feature_mat_hypothesis(self):
        exception_hypotheses = ["Communication", "Uncertain"]
        return [
            hypothesis
            for hypothesis in self.test_hypotheses
            if hypothesis not in exception_hypotheses
        ]
