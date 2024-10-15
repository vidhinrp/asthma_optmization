import asthma_cost_eval.input_data as data
import asthma_cost_eval.model_classes as model
import asthma_cost_eval.param_classes as param
import asthma_cost_eval.support as support

# simulating daily therapy
# create a cohort
cohort_daily = model.Cohort(id=0,
                           pop_size=data.POP_SIZE,
                           parameters=param.Parameters(therapy=param.Therapies.DAILY))
# simulate the cohort
cohort_daily.simulate(n_time_steps=data.SIM_TIME_STEPS)

# simulating intermittent therapy
# create a cohort
cohort_inter = model.Cohort(id=1,
                            pop_size=data.POP_SIZE,
                            parameters=param.Parameters(therapy=param.Therapies.INTERMITTENT))
# simulate the cohort
cohort_inter.simulate(n_time_steps=data.SIM_TIME_STEPS)

# print the estimates for the mean survival time and mean time to AIDS
support.print_outcomes(sim_outcomes=cohort_daily.cohortOutcomes,
                       therapy_name=param.Therapies.DAILY)
support.print_outcomes(sim_outcomes=cohort_inter.cohortOutcomes,
                       therapy_name=param.Therapies.INTERMITTENT)

# print comparative outcomes
support.print_comparative_outcomes(sim_outcomes_daily=cohort_daily.cohortOutcomes,
                                   sim_outcomes_inter=cohort_inter.cohortOutcomes)

# report the CEA results
support.report_CEA_CBA(sim_outcomes_daily=cohort_daily.cohortOutcomes,
                       sim_outcomes_inter=cohort_inter.cohortOutcomes)
