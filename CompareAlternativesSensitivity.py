import asthma_cost_eval.input_data as data
import asthma_param_uncertainity.model_classes as model
import asthma_param_uncertainity.param_classes as param
import asthma_param_uncertainity.support as support

N_COHORTS = 1000  # number of cohorts
POP_SIZE = 259  # population size of each cohort

# create a multi-cohort to simulate under mono therapy
multiCohortDAILY = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    therapy=param.Therapies.DAILY
)

multiCohortDAILY.simulate(n_time_steps=data.SIM_TIME_STEPS)

# create a multi-cohort to simulate under combo therapy
multiCohortINTER = model.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    therapy=param.Therapies.INTERMITTENT
)

multiCohortINTER.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time and mean time to AIDS
support.print_outcomes(multi_cohort_outcomes=multiCohortDAILY.multiCohortOutcomes,
                       therapy_name=param.Therapies.DAILY)

support.print_outcomes(multi_cohort_outcomes=multiCohortINTER.multiCohortOutcomes,
                       therapy_name=param.Therapies.INTERMITTENT)

# print comparative outcomes
support.print_comparative_outcomes(multi_cohort_outcomes_daily=multiCohortDAILY.multiCohortOutcomes,
                                   multi_cohort_outcomes_inter=multiCohortINTER.multiCohortOutcomes)

# report the CEA results
support.report_CEA_CBA(multi_cohort_outcomes_daily=multiCohortDAILY.multiCohortOutcomes,
                       multi_cohort_outcomes_inter=multiCohortINTER.multiCohortOutcomes)