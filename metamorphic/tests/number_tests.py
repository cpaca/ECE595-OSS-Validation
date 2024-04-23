import numpy

import DFBuilder
from test_functions import assert_dfs_equal, mark_as_metamorphic_test


@mark_as_metamorphic_test
def test_addition(dfb: DFBuilder.DFBuilder):
    ret = [dfb.deepcopy()]
    # Make sure this is a multiply-able class.
    if not dfb.check_types((int, float, complex)):
        return ret

    # Add 7 and add 24. Numbers chosen to find problems more "obviously"
    # You know what? Subtract 11 and 29 too.
    for const in [7, 24, -11, -29]:
        df = dfb.to_df()
        df += const

        dfb2 = dfb.map_elements(lambda i: i + const)
        df2 = dfb2.to_df()

        # f(df(x)) is doing math directly to df
        # df(f(x)) is inserting numbers directly to df
        assert_dfs_equal(df, df2, dfb.count_asserts)

        ret.append(dfb2)
    return ret


@mark_as_metamorphic_test
def test_absolute_value(dfb: DFBuilder.DFBuilder):
    ret = [dfb.deepcopy()]
    # Make sure this is a numerical class.
    if not dfb.check_types((int, float, complex)):
        return ret

    df = dfb.to_df()
    df = df.abs()

    dfb2 = dfb.map_elements(lambda x: abs(x))
    df2 = dfb2.to_df()

    # f(df(x)) is doing math directly to df (df.abs)
    # df(f(x)) is doing math to the data (abs(x))
    assert_dfs_equal(df, df2, dfb.count_asserts)

    ret.append(dfb2)
    return ret


@mark_as_metamorphic_test
def test_inversion(dfb: DFBuilder.DFBuilder):
    ret = [dfb.deepcopy()]
    # Make sure this is a numerical class.
    if not dfb.check_types((int, float, complex)):
        return ret

    df = dfb.to_df()
    df = 1/df

    # Don't want the divide-by-zero errors
    with numpy.errstate(divide="ignore"):
        dfb2 = dfb.map_elements(lambda x: numpy.divide(1, x))
    df2 = dfb2.to_df()

    # f(df(x)) is doing math directly to df (1/df)
    # df(f(x)) is doing math to the data (df/1)
    assert_dfs_equal(df, df2, dfb.count_asserts)

    ret.append(dfb2)
    return ret
