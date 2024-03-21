import numpy as np
import pandas as pd


class DempsterShafer:
    """
    This class provides methods to calculate Dempster's rule
    """

    def __init__(self, sampling_matrix=None, feature_matrix=None):
        if sampling_matrix is not None and feature_matrix is not None:
            self.sampling_matrix = sampling_matrix
            self.feature_matrix = feature_matrix

            self.num_hypos = feature_matrix.shape[0]
            self.num_feats = feature_matrix.shape[1]
            self.num_samples = sampling_matrix.shape[0]
        else:
            # No input provided
            pass

    def hypothesis_order(self, hypothesis):
        """
        This method takes a list of hypotheses and assigns them accordingly
        """
        # print(hypothesis)
        if len(hypothesis) == (self.feature_matrix.shape[0] + 1):
            # Length of hypothesis is equal to the number of rows of feature_matrix
            self.hypotheses = hypothesis
        else:
            print(
                "List of hypotheses does not align to the number of rows of feature matrix"
            )

    def result(self):
        distance_matrix = self.distance_matrix(
            self.sampling_matrix, self.feature_matrix
        )
        probability_matrix = self.probability_matrix(distance_matrix)
        shannon_entropy = self.shannon_entropy(probability_matrix)
        discount_factor = self.discounting_factor(shannon_entropy)
        discounted_BPA = self.multiplyDiscountFactor(
            discount_factor, probability_matrix
        )
        final_mass_function = self.samplings_combined_mass_function(discounted_BPA)
        if hasattr(self, "hypotheses") and self.hypotheses:
            result_df = pd.DataFrame(
                {
                    hypothesis: [final_mass_function[i]]
                    for i, hypothesis in enumerate(self.hypotheses)
                }
                # index=[0],  # Example index, you can adjust it as needed
            )
        else:
            num_hypotheses = len(final_mass_function)
            result_df = pd.DataFrame(
                {f"H{i+1}": final_mass_function[i] for i in range(num_hypotheses)}
            )

        return result_df

    # Define other functions as class methods

    # Method to calculate distance matrix
    def distance_matrix(self, sampling_mat, feature_mat):
        num_samplings = sampling_mat.shape[0]
        num_hypos, num_features = feature_mat.shape[0], feature_mat.shape[1]
        distance_mat = np.zeros((num_hypos, num_samplings, num_features))

        for i in range(num_samplings):
            distance_mat[:, i, :] = np.abs(sampling_mat[i, :] - feature_mat)

        # print("Distance matrix: ", distance_mat)
        return distance_mat

    # Method to calculate probability matrix
    def probability_matrix(self, distance_matrix):
        probability = 1.0 / distance_matrix
        sum_probability = np.sum(probability, axis=0)
        normalised_probability = probability / sum_probability
        normalised_probability = np.where(
            np.isnan(normalised_probability), 0, normalised_probability
        )
        # print("Normalised: ", normalised_probability)
        return normalised_probability

    # Method to calculate Shannon entropy
    def shannon_entropy(self, probability):
        epsilon = 1  # Small positive value to prevent log(0)
        probability = np.where(
            np.isnan(probability) | (probability == 0), epsilon, probability
        )
        entropy = -np.sum(probability * np.log(probability), axis=0)
        # print("Entropy: ", entropy)
        return entropy

    # Method to calculate discount factor
    def discounting_factor(self, entropy):
        variance = np.var(entropy, ddof=1)
        discount_factor = 1 - (entropy / (entropy + variance))
        # print("Discount: ", discount_factor)
        return discount_factor

    # Method to take into account discount factor
    def multiplyDiscountFactor(self, discount_mat: np.ndarray, prob_mat):
        """
        Parameters:
            ----------
            discount_mat : numpy.ndarray
                The discount factor matrix with shape (M, N), where M and N are the dimensions of the matrix.
            prob_mat : numpy.ndarray
                The probability matrix with shape LxMxN.

        Returns:
            -------
            numpy.ndarray
                The discounted probability matrix with the shape LxMx(N+1).
        """
        # Get the size (depth) of the probability matrix
        num_hypos = len(prob_mat)  # len gets outermost dimension

        # Expand the discount factor matrix to match the size of the probability matrix
        expanded_discount_mat = np.tile(
            discount_mat, (num_hypos, 1, 1)
        )  # tile replicate the matrix

        # Multiply the discount factor matrix with the probability matrix element-wise
        discounted_prob_matrix = prob_mat * expanded_discount_mat

        # Calculate the last layer of the discounted_prob_matrix as 1 minus the sum along the third dimension
        uncertainty_layer = 1 - np.sum(
            discounted_prob_matrix, axis=0, keepdims=True
        )  # This is the uncertainty hypothesis

        # Stack the uncertainty_layer to discounted_prob_matrix along the third dimension
        discounted_prob_matrix = np.vstack((discounted_prob_matrix, uncertainty_layer))
        # print("Discounted probability matrix: ", discounted_prob_matrix)
        return discounted_prob_matrix

    def samplings_combined_mass_function(self, discounted_bpa):
        """
        Parameters:
            discounted_bpa : numpy.ndarray
                The sampling matrix with shape (L, M, N+1).

        Returns:
            numpy.ndarray
                The combined mass function matrix with shape (1, N+1).
        """
        num_samplings, num_hypos = discounted_bpa.shape[1], discounted_bpa.shape[0]
        ds = np.zeros((num_samplings, num_hypos))
        # print("DS: ", ds)
        for i in range(num_samplings):
            # Calculate the combined mass function for each sampling
            # Transpose to combine evidence consecutively feature-wise
            ds[i, :] = self.combined_mass_function(discounted_bpa[:, i, :].transpose())

        # Calculate the combined mass function for all samplings
        return self.combined_mass_function(ds)

    # Method to get combined mass function
    def combined_mass_function(self, mass_func):
        # print("Mass: ", mass_func)
        num_hypos = mass_func.shape[1]
        inter_steps = mass_func.shape[0] - 1
        step_mass_function = np.zeros_like(mass_func)
        step_mass_function[0, :] = mass_func[0, :]

        inter_mass_func = np.zeros((inter_steps, num_hypos, num_hypos))
        # Conflict coefficient
        k = np.zeros(inter_steps)

        for j in range(inter_steps):
            # Calculate the intermediate combined mass function of a pair of consecutive pieces of evidence
            # for i in range(num_hypos):
            #     inter_mass_func[j, :, i] = (
            #         step_mass_function[j, i] * mass_func[j + 1, :]
            #     )
            inter_mass_func[j, :, :] = np.outer(
                step_mass_function[j, :], mass_func[j + 1, :]
            )

            # print("Inter mass: ", inter_mass_func)
            # Calculate the conflict coefficient
            d = np.diag(inter_mass_func[j, :, : (num_hypos - 1)])
            # print("d: ", d)
            k[j] = np.sum(inter_mass_func[j, :-1, :-1]) - np.sum(d)

            # Calculation of combined intermediate mass function
            for i in range(num_hypos - 1):
                step_mass_function[j + 1, i] = (
                    inter_mass_func[j, i, i]
                    + inter_mass_func[j, i, num_hypos - 1]
                    + inter_mass_func[j, num_hypos - 1, i]
                ) / (1 - k[j])

            step_mass_function[j + 1, num_hypos - 1] = inter_mass_func[
                j, num_hypos - 1, num_hypos - 1
            ] / (1 - k[j])
        # print("Step: ", step_mass_function[-1, :])
        return step_mass_function[-1, :]
