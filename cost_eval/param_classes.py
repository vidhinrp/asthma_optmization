from enum import Enum
import asthma_cost_eval.input_data as data


class Therapies(Enum):
    """ daily vs intermittent therapy """
    DAILY = 0
    INTERMITTENT = 1


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = data.HealthStates.WELL

        # annual treatment cost
        self.annualTreatmentCost = 0

        # transition probability matrix of the selected therapy
        self.probMatrix = []

        # calculate transition probabilities
        if self.therapy == Therapies.DAILY:
            # calculate transition probability matrix for the daily therapy
            self.probMatrix = data.S_TRANS_MATRIX_DAILY
            self.annualStateCosts = data.S_HEALTH_COST_DAILY

        elif self.therapy == Therapies.INTERMITTENT:
            # calculate transition probability matrix for intermittent therapy
            self.probMatrix = data.S_TRANS_MATRIX_INTERMITTENT
            self.annualStateCosts = data.S_HEALTH_COST_INTERMITTENT

        # annual state costs and utilities
        self.annualStateUtilities = data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = 0


if __name__ == '__main__':
    matrix_daily = data.S_TRANS_MATRIX_DAILY
    matrix_inter = data.S_TRANS_MATRIX_INTERMITTENT

    print(matrix_daily)
    print(matrix_inter)
