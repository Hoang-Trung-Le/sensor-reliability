import numpy as np


class DempsterShafer:
    """
    This class provides methods to calculate Dempster's rule
    """

    def __init__(self):
        pass  # You can add any initialization code here

    def result(self, sampling_matrix, feature_matrix):
        distance_matrix = self.distance_matrix(sampling_matrix, feature_matrix)
        probability_matrix = self.probability_matrix(distance_matrix)
        shannon_entropy = self.shannon_entropy(probability_matrix)
        discount_factor = self.discounting_factor(shannon_entropy)
        discounted_BPA = self.multiplyDiscountFactor(
            discount_factor, probability_matrix
        )
        final_mass_function = self.samplings_combined_mass_function(discounted_BPA)

        return final_mass_function

    # Define other functions as class methods

    # Method to calculate distance matrix
    def distance_matrix(self, sampling_mat, feature_mat):
        num_samplings = sampling_mat.shape[0]
        num_hypos, num_features = feature_mat.shape[0], feature_mat.shape[1]
        distance_mat = np.zeros((num_hypos, num_samplings, num_features))

        for i in range(num_samplings):
            distance_mat[:, i, :] = np.abs(sampling_mat[i, :] - feature_mat)

        print("Distance matrix: ", distance_mat)
        return distance_mat

    # Method to calculate probability matrix
    def probability_matrix(self, distance_matrix):
        probability = 1.0 / distance_matrix
        sum_probability = np.sum(probability, axis=0)
        normalised_probability = probability / sum_probability

        print("Normalised: ", normalised_probability)
        return normalised_probability

    # Method to calculate Shannon entropy
    def shannon_entropy(self, probability):
        entropy = -np.sum(probability * np.log(probability), axis=0)
        print("Entropy: ", entropy)
        return entropy

    # Method to calculate discount factor
    def discounting_factor(self, entropy):
        variance = np.var(entropy, ddof=1)
        discount_factor = 1 - (entropy / (entropy + variance))
        print("Discount: ", discount_factor)
        return discount_factor

    # Method to take into account discount factor
    def multiplyDiscountFactor(self, discountMatrix: np.ndarray, probMatrix):
        """
        Parameters:
            ----------
            discountMatrix : numpy.ndarray
                The discount factor matrix with shape (M, N), where M and N are the dimensions of the matrix.
            probMatrix : numpy.ndarray
                The probability matrix with shape (M, N, P), where P is the number of features.

        Returns:
            -------
            numpy.ndarray
                The result matrix with the same shape as probMatrix.
        """
        # Get the size (depth) of the probability matrix
        numFeatures = len(probMatrix)

        # Expand the discount factor matrix to match the size of the probability matrix
        expandedDiscountMatrix = np.tile(discountMatrix, (numFeatures, 1, 1))

        # Multiply the discount factor matrix with the probability matrix element-wise
        resultMatrix = probMatrix * expandedDiscountMatrix

        # Calculate the last layer of the resultMatrix as 1 minus the sum along the third dimension
        last_layer = 1 - np.sum(resultMatrix, axis=0, keepdims=True)

        # Stack the last_layer to resultMatrix along the third dimension
        resultMatrix = np.vstack((resultMatrix, last_layer))
        print("Result: ", resultMatrix)
        return resultMatrix

    # Method to obtain combined mass function
    """

    """

    def samplings_combined_mass_function(self, sampling_mat):
        num_samplings, num_hypos = sampling_mat.shape[1], sampling_mat.shape[0]
        ds = np.zeros((num_samplings, num_hypos))

        for i in range(num_samplings):
            ds[i, :] = self.combined_mass_function(sampling_mat[i, :, :])

        return self.combined_mass_function(ds)

    # Method to get combined mass function
    def combined_mass_function(self, mass_func):
        num_hypos = mass_func.shape[1]
        inter_steps = mass_func.shape[0] - 1
        step_mass_function = np.zeros_like(mass_func)
        step_mass_function[0, :] = mass_func[0, :]

        inter_mass_func = np.zeros((inter_steps, num_hypos, num_hypos))
        k = np.zeros(inter_steps)

        for j in range(inter_steps):
            # Calculate the intermediate combined mass function of a pair of consecutive pieces of evidence
            for i in range(num_hypos):
                inter_mass_func[:, i, j] = (
                    step_mass_function[j, i] * mass_func[j + 1, :]
                )

            # Calculate the conflict coefficient
            d = np.diag(inter_mass_func[:, : (num_hypos - 1), j])
            k[j] = np.sum(inter_mass_func[:-1, :-1, j]) - np.sum(d)

            # Calculation of combined intermediate mass function
            for i in range(num_hypos - 1):
                step_mass_function[j + 1, i] = (
                    inter_mass_func[i, i, j]
                    + inter_mass_func[i, num_hypos - 1, j]
                    + inter_mass_func[num_hypos - 1, i, j]
                ) / (1 - k[j])

            step_mass_function[j + 1, num_hypos - 1] = inter_mass_func[
                num_hypos - 1, num_hypos - 1, j
            ] / (1 - k[j])

        return step_mass_function[-1, :]
