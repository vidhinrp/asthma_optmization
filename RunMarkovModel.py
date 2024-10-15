import asthma_cost_eval.input_data as data
import asthma_cost_eval.model_classes as model
import asthma_cost_eval.param_classes as param
import asthma_cost_eval.support as Support

# selected therapy
therapy = param.Therapies.DAILY

# create a cohort
myCohort = model.Cohort(id=1,
                        pop_size=data.POP_SIZE,
                        parameters=param.Parameters(therapy=therapy))

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=data.SIM_TIME_STEPS)


# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,
                       therapy_name=therapy)
