import deampy.random_variates as rvgs
import numpy as np


import asthma_cost_eval.input_data as data
from asthma_cost_eval.param_classes import Therapies


class Parameters:
    """ class to include parameter information to simulate the model """

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = data.HealthStates.WELL     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.probMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = data.DISCOUNT   # discount rate


class ParameterGenerator:
    """ class to generate parameter values from the selected probability distributions """

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of beta distributions for transition probabilities
        self.annualStateCostRVGs = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVGs = []  # list of gamma distributions for the annual utility of states
        self.annualTreatmentCost = 0
        # create beta distribution for transition probabilities
        if self.therapy == Therapies.DAILY:
            fit_output_ws = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_DAILY[0][1],
                                             st_dev=data.S_TRANS_MATRIX_DAILY[0][1] / 4)
            fit_output_ss = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_DAILY[1][1],
                                             st_dev=data.S_TRANS_MATRIX_DAILY[1][1] / 4)
            fit_output_as = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_DAILY[2][1],
                                             st_dev=data.S_TRANS_MATRIX_DAILY[2][1] / 4)

            self.probMatrixRVG = [
                [rvgs.Beta(106.106, 7.607),  # WELL
                 rvgs.Beta(a=fit_output_ws["a"], b=fit_output_ws["b"]),
                 rvgs.Beta(396.254, 42029.30)],
                [rvgs.Beta(44.313, 5.645),  # SUBOPTIMAL
                 rvgs.Beta(a=fit_output_ss["a"], b=fit_output_ss["b"]),
                 rvgs.Beta(393.584, 393.584)],
                [rvgs.Beta(297.745, 869.882),  # ASTHMA
                 rvgs.Beta(a=fit_output_as["a"], b=fit_output_as["b"]),
                 rvgs.Beta(395.148, 32261.70)],
            ]

            self.annualTreatmentCost=rvgs.Gamma(25.60, 0.64)

        if self.therapy == Therapies.INTERMITTENT:
            fit_output_ws = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_INTERMITTENT[0][1],
                                             st_dev=data.S_TRANS_MATRIX_INTERMITTENT[0][1] / 4)
            fit_output_ss = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_INTERMITTENT[1][1],
                                             st_dev=data.S_TRANS_MATRIX_INTERMITTENT[1][1] / 4)
            fit_output_as = rvgs.Beta.fit_mm(mean=data.S_TRANS_MATRIX_INTERMITTENT[2][1],
                                             st_dev=data.S_TRANS_MATRIX_INTERMITTENT[2][1] / 4)

            self.probMatrixRVG = [
                [rvgs.Beta(226.582, 37.545),  # WELL
                 rvgs.Beta(a=fit_output_ws["a"], b=fit_output_ws["b"]),
                 rvgs.Beta(395.869, 38038.08)],
                [rvgs.Beta(72.383, 16.213),  # SUBOPTIMAL
                 rvgs.Beta(a=fit_output_ss["a"], b=fit_output_ss["b"]),
                 rvgs.Beta(390.777, 16599.53)],
                [rvgs.Beta(357.895, 3050.629),  # ASTHMA
                 rvgs.Beta(a=fit_output_as["a"], b=fit_output_as["b"]),
                 rvgs.Beta(392.942, 21933.33)],
            ]

        # create gamma distributions for annual state cost
        self.annualStateCostRVGs = [rvgs.Gamma(44.444, .21063),    # WELL
                                    rvgs.Gamma(44.444, 1.353),   # SUBOPTIMAL
                                    rvgs.Normal(5.477, 1.006),  # ASTHMA
                                    ]




        # create beta distributions for annual utility cost
        self.annualStateUtilityRVGs = [rvgs.Beta(3.411, 0.038),  # WELL
                                       rvgs.Beta(117.295, 49.081),  # SUBOPTIMAL
                                       rvgs.Beta(289.725, 763.820),  # ASTHMA
                                       ]

    def get_new_parameters(self, seed):
        """
        :param seed: seed for the random number generator used to a sample of parameter values
        :return: a new parameter set
        """

        rng = np.random.RandomState(seed=seed)

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # calculate transition probabilities
        prob_matrix = []  # probability matrix without background mortality added
        # for all health states
        for row in self.probMatrixRVG:
            x = []
            for dist in row:
                x.append(dist.sample(rng))
            prob_matrix.append(x)

        # Normalize each row so that the sum of each row equals 1
        for row in prob_matrix:
            row_sum = sum(row)
            # If row_sum is not 1, normalize the row
            if row_sum != 1.0:
                row[:] = [value / row_sum for value in row]

        # Assign prob_matrix to param.probMatrix
        param.probMatrix = prob_matrix

        if self.annualTreatmentCost!=0:
            daily_cost = self.annualTreatmentCost.sample(rng)
        else:
            daily_cost =0

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.annualStateCostRVGs:
            param.annualStateCosts.append(dist.sample(rng)+daily_cost)

        # sample from beta distributions that are assumed for annual state utilities
        for dist in self.annualStateUtilityRVGs:
            param.annualStateUtilities.append(dist.sample(rng))

        # return the parameter set
        return param
