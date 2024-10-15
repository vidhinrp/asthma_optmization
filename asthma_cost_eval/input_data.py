from enum import Enum

# simulation settings
POP_SIZE = 10000        # cohort population size
SIM_TIME_STEPS = 52   # length of simulation (weeks)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0    # annual discount rate


class HealthStates(Enum):
    """ health states of patients"""
    WELL = 0
    SUBOPTIMAL = 1
    ASTHMA = 2

# School children - Transition matrix for daily therapy
S_TRANS_MATRIX_DAILY = [
    [0.933, 0.058, 0.009],   # WELL
    [0.887, 0.097, 0.016],   # SUBOPTIMAL
    [0.255, 0.733, 0.012],   # ASTHMA
]

# School children - Transition matrix for intermittent therapy
S_TRANS_MATRIX_INTERMITTENT = [
    [0.858, 0.132, 0.010],   # WELL
    [0.817, 0.160, 0.023],   # SUBOPTIMAL
    [0.105, 0.878, 0.017],   # ASTHMA
]

# Preschool children - Transition matrix for daily therapy
PS_TRANS_MATRIX_DAILY = [
    [0.810, 0.181, 0.009],   # WELL
    [0.520, 0.464, 0.016],   # SUBOPTIMAL
    [0.255, 0.723, 0.022],   # ASTHMA
]

# Preschool children - Transition matrix for intermittent therapy
PS_TRANS_MATRIX_INTERMITTENT = [
    [0.780, 0.210, 0.010],   # WELL
    [0.450, 0.529, 0.021],   # SUBOPTIMAL
    [0.105, 0.876, 0.019],   # ASTHMA
]

# Health cost matrix for school patients - Daily ICS
S_HEALTH_COST_DAILY = [
    2.51,   # WELL
    33.23,  # SUBOPTIMAL
    397.40, # ASTHMA
]

# Health cost matrix for school patients - Intermittent ICS
S_HEALTH_COST_INTERMITTENT = [
    2.11,   # WELL
    32.83,  # SUBOPTIMAL
    397.40, # ASTHMA
]

# Health cost matrix for preschool patients - Daily ICS
PS_HEALTH_COST_DAILY = [
    2.70,   # WELL
    33.42,  # SUBOPTIMAL
    397.59, # ASTHMA
]

# Health cost matrix for preschool patients - Intermittent ICS
PS_HEALTH_COST_INTERMITTENT = [
    2.11,   # WELL
    32.83,  # SUBOPTIMAL
    397.59, # ASTHMA
]


# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    0.989,  # WELL
    0.705,  # SUBOPTIMAL
    0.275,    # ASTHMA
    ]
