import deampy.econ_eval as econ
import deampy.statistics as stat


import asthma_cost_eval.input_data as data


def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """

    # mean and confidence interval text of time to asthma
    time_to_asthma_CI_text = sim_outcomes.statTimeToAsthma.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=0, form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean time to Asthma and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          time_to_asthma_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")



def print_comparative_outcomes(sim_outcomes_daily, sim_outcomes_inter):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under intermittent therapy compared to daily therapy
    :param sim_outcomes_daily: outcomes of a cohort simulated under daily therapy
    :param sim_outcomes_inter: outcomes of a cohort simulated under intermittent therapy
    """

    # increase in mean discounted cost under intermittent therapy with respect to daily therapy
    increase_discounted_cost = stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_inter.costs,
        y_ref=sim_outcomes_daily.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)

    # increase in mean discounted utility under intermittent therapy with respect to daily therapy
    increase_discounted_utility = stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_inter.utilities,
        y_ref=sim_outcomes_daily.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(
        interval_type='c', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - data.ALPHA, prec=0), estimate_CI)


def report_CEA_CBA(sim_outcomes_daily, sim_outcomes_inter):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_daily: outcomes of a cohort simulated under daily therapy
    :param sim_outcomes_inter: outcomes of a cohort simulated under intermittent therapy
    """

    # define two strategies
    daily_therapy_strategy = econ.Strategy(
        name='Daily Therapy',
        cost_obs=sim_outcomes_daily.costs,
        effect_obs=sim_outcomes_daily.utilities,
        color='green'
    )
    inter_therapy_strategy = econ.Strategy(
        name='Intermittent Therapy',
        cost_obs=sim_outcomes_inter.costs,
        effect_obs=sim_outcomes_inter.utilities,
        color='blue'
    )

    # do CEA
    # (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
    CEA = econ.CEA(
        strategies=[daily_therapy_strategy, inter_therapy_strategy],
        if_paired=False
    )

    # plot cost-effectiveness figure
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional QALYs',
        y_label='Additional Cost',
        interval_type='c',  # to show confidence intervals for cost and effect of each strategy
        file_name='figs/cea.png'
    )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    CBA = econ.CBA(
        strategies=[daily_therapy_strategy, inter_therapy_strategy],
        wtp_range=[0, 100000],
        if_paired=False
    )
    # show the net monetary benefit figure
    CBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per QALY ($)',
        y_label='Marginal Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/nmb.png'
    )
