import deampy.econ_eval as econ
import deampy.statistics as stat

import asthma_cost_eval.input_data as data


def print_outcomes(multi_cohort_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """

    # mean and prediction interval text of time to AIDS
    time_to_asthma_Exarcebation_PI_text = multi_cohort_outcomes.statMeanTimeToAsthma.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2, form=',')

    # mean and prediction interval text of discounted total QALY
    utility_mean_PI_text = multi_cohort_outcomes.statMeanQALY.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean time to asthma exacerbation and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          time_to_asthma_Exarcebation_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          cost_mean_PI_text)
    print("  Estimate of mean discounted utility and {:.{prec}%} uncertainty interval:".format(1 - data.ALPHA, prec=0),
          utility_mean_PI_text)
    print("")


def print_comparative_outcomes(multi_cohort_outcomes_daily, multi_cohort_outcomes_inter):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under daily therapy compared to intermittent therapy
    :param multi_cohort_outcomes_daily: outcomes of a multi-cohort simulated under daily therapy
    :param multi_cohort_outcomes_inter outcomes of a multi-cohort simulated under intermittent therapy
    """

    # increase in mean asthma exacerbation time under intermittent therapy with respect to daily therapy
    increase_mean_survival_time = stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_inter.meanTimeToAsthma,
        y_ref=multi_cohort_outcomes_daily.meanTimeToAsthma)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)
    print("Increase in mean asthma exacerbation time and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

    # increase in mean discounted cost under intermittent therapy with respect to daily therapy
    increase_mean_discounted_cost = stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_inter.meanCosts,
        y_ref=multi_cohort_outcomes_daily.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2, form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

    # increase in mean discounted QALY under intermittent therapy with respect to daily therapy
    increase_mean_discounted_qaly = stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_cohort_outcomes_inter.meanQALYs,
        y_ref=multi_cohort_outcomes_daily.meanQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(
        interval_type='p', alpha=data.ALPHA, deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - data.ALPHA, prec=0), estimate_PI)

def report_CEA_CBA(multi_cohort_outcomes_daily, multi_cohort_outcomes_inter):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_daily: outcomes of a multi-cohort simulated under daily therapy
    :param multi_cohort_outcomes_inter: outcomes of a multi-cohort simulated under intermittent therapy
    """

    # define two strategies
    daily_therapy_strategy = econ.Strategy(
        name='Daily ICS Therapy',
        cost_obs=multi_cohort_outcomes_daily.meanCosts,
        effect_obs=multi_cohort_outcomes_daily.meanQALYs,
        color='green'
    )
    inter_therapy_strategy = econ.Strategy(
        name='Intermittent ICS Therapy',
        cost_obs=multi_cohort_outcomes_inter.meanCosts,
        effect_obs=multi_cohort_outcomes_inter.meanQALYs,
        color='blue'
    )

    # do CEA
    CEA = econ.CEA(
        strategies=[daily_therapy_strategy, inter_therapy_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional Discounted QALY',
        y_label='Additional Discounted Cost',
        fig_size=(6, 5),
        add_clouds=True,
        transparency=0.2,
        file_name='figs/cea_sensitivity.png')

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # uncertainty (projection) interval for cost and effect estimates but
                            # for ICER, confidence interval will be reported.
        alpha=data.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable_sensitivity.csv')

    # CBA
    NBA = econ.CBA(
        strategies=[daily_therapy_strategy, inter_therapy_strategy],
        wtp_range=(0, 50000),
        if_paired=True
    )
    # show the net monetary benefit figure
    NBA.plot_marginal_nmb_lines(
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c', # show confidence interval
        show_legend=True,
        figure_size=(6, 5),
        file_name='figs/nmb_sensitivity.png'
    )