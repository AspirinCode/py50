"""
Script to calculate statistics.
"""

from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from statannotations.Annotator import Annotator
from py50 import utils


class Stats:
    """
    Class contains wrappers for pingouin module. These are statistical outputs for a given input. The functions are in
    a format needed for plotting in class Plots(), however they can also be used individually to output single DataFrame
    with statistical calculations for a given dataset.
    """

    def __init__(self):
        pass

    # todo add kwargs options for all dataframes to feed into pg
    @staticmethod
    def get_t_test(df, paired=True, stars=False, decimals=4, **kwargs):
        """
        Calculate pairwise t-test.
        :param df:
        :param paired:
        :param stars:
        :param decimals:
        :param kwargs:
        :return:
        """
        result_df = pg.ptests(
            data=df, paired=paired, stars=stars, decimals=decimals, **kwargs
        )
        return result_df

    @staticmethod
    def get_normality(df, dv=None, group=None, **kwargs):
        """

        :param df:
        :param dv:
        :param group:
        :param method:
        :return:
        """

        result_df = pg.normality(data=df, dv=dv, group=group, **kwargs)
        return result_df

    @staticmethod
    def get_homoscedasticity(df, dv=None, group=None, **kwargs):
        """

        :param df:
        :param dv:
        :param group:
        :param kwargs:
        :return:
        """

        result_df = pg.homoscedasticity(data=df, dv=dv, group=group, **kwargs)
        return result_df

    @staticmethod
    def get_anova(df, dv=None, between=None, **kwargs):
        """

        :param df:
        :param dv:
        :param between:
        :param type:
        :return:
        """

        result_df = pg.anova(data=df, dv=dv, between=between, **kwargs)
        return result_df

    # todo check if **kwarg needed. Only need to add the option within the pg. function
    @staticmethod
    def get_tukey(df, dv=None, between=None, **kwargs):
        """

        :param df:
        :param dv:
        :param between:
        :return:
        """
        result_df = pg.pairwise_tukey(data=df, dv=dv, between=between, **kwargs)
        return result_df

    @staticmethod
    def get_gameshowell(df, dv=None, between=None, **kwargs):
        result_df = pg.pairwise_gameshowell(data=df, dv=dv, between=between, **kwargs)
        return result_df

    @staticmethod
    def get_p_test(df, dv=None, between=None, **kwargs):
        """
        Calculate pairwise_tests
        :param df:
        :param dv:
        :param between:
        :param effsize:
        :param kwargs:
        :return:
        """
        result_df = pg.pairwise_tests(data=df, dv=dv, between=between, **kwargs)
        return result_df

    @staticmethod
    def get_rm_anova(df, dv=None, within=None, subject=None, **kwargs):
        result_df = pg.rm_anova(data=df, dv=dv, within=within, subject=subject, **kwargs)
        return result_df

    @staticmethod
    def get_mixed_anova(df, dv=None, within=None, subject=None, **kwargs):
        result_df = pg.mixed_anova(data=df, dv=dv, within=within, subject=subject, **kwargs)
        return result_df


class Plots:

    @staticmethod
    def box_plot(
        df,
        x_axis=None,
        y_axis=None,
        group_col=None,
        test=None,
        return_df=None,
        palette=None,
        savepath=None,
        **kwargs
    ):
        """

        :param df:
        :param x_axis:
        :param y_axis:
        :param group_col:
        :param test:
        :param return_df: Will return dataframe of calculated results
        :param palette:
        :return:
        """

        # pairs = list(combinations(df[group_col].unique(), 2))
        groups = df[group_col].unique()

        # set default color palette
        if palette is not None:
            palette = utils.palette(palette)
        ax = sns.boxplot(data=df, x=x_axis, y=y_axis, order=groups, palette=palette)

        try:
            # Run tests based on test parameter input
            if test is not None:
                pvalue, test_df = _get_test(
                    test=test, df=df, x_axis=x_axis, y_axis=y_axis, **kwargs
                )
            else:
                raise NameError("Must include test as: 'tukey', 'gameshowell', 'ttest'")

            pair_plot = [(a, b) for a, b in zip(test_df["A"], test_df["B"])]

            # add annotations
            annotator = Annotator(
                ax, pair_plot, data=df, x=x_axis, y=y_axis, verbose=False
            )
            annotator.set_custom_annotations(pvalue)
            annotator.annotate()
            if savepath:
                plt.savefig(savepath, dpi=300, bbox_inches="tight")
        except ValueError:
            print("Input test type! Use 'tukey', 'gameshowell', or 'ttest'")

        if return_df:
            return test_df  # return calculated df. Change name for more description

    # todo Include plots for ttest. This requires different inputs in pg
    @staticmethod
    def ttest_bar_plot(
        df,
        x_axis=None,
        y_axis=None,
        group_col=None,
        test=None,
        return_df=None,
        palette=None,
    ):

        pairs = list(combinations(df[group_col].unique(), 2))
        groups = df[group_col].unique()

        # set default color palette
        if palette is not None:
            palette = utils.palette(palette)
        ax = sns.boxplot(data=df, x=x_axis, y=y_axis, order=groups, palette=palette)

        try:
            # Run tests based on test parameter input
            if test is not None:
                pvalue, test_df = _get_test(
                    test=test, df=df, x_axis=x_axis, y_axis=y_axis
                )
            else:
                raise NameError("Must include test as: 'tukey', 'gameshowell', 'ttest'")

            pair_plot = [(a, b) for a, b in zip(test_df["A"], test_df["B"])]

            # add annotations
            annotator = Annotator(
                ax, pair_plot, data=df, x=x_axis, y=y_axis, verbose=False
            )
            annotator.set_custom_annotations(pvalue)
            annotator.annotate()
        except ValueError:
            print("Input test type! Use 'tukey', 'gameshowell', or 'ttest'")

        if return_df:
            return test_df  # return calculated df. Change name for more description


def _get_test(test, df=None, x_axis=None, y_axis=None, **kwargs):
    """
    Function to utilize a specific statistical test. This will output the results in a dataframe and also the pvalues as
    a list. This function is primarily used for the plot functions in the stats.Plots() class.

    :param test:
    :param df:
    :param x_axis:
    :param y_axis:
    :param kwargs:
    :return:
    """
    # todo expand the kwargs for other tests. May need to refactor this afterwards
    if test == "tukey":
        effsize = kwargs.get("effsize")
        if effsize is None:
            effsize = "hedges"
        test_df = Stats.get_tukey(df, dv=y_axis, between=x_axis, effsize=effsize)
        pvalue = [utils.star_value(value) for value in test_df["p-tukey"].tolist()]
    elif test == "gameshowell":
        test_df = Stats.get_gameshowell(df, dv=y_axis, between=x_axis)
        pvalue = [utils.star_value(value) for value in test_df["pval"].tolist()]
    elif test == "ptest":
        test_df = Stats.get_ttest(df, dv=y_axis, between=x_axis)
        pvalue = [utils.star_value(value) for value in test_df["p-unc"].tolist()]

    return (
        pvalue,
        test_df,
    )  # need to return both the pvalue as a list and the calculated df


if __name__ == "__main__":
    import doctest

    doctest.testmod()
