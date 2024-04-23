import DFBuilder
from test_functions import assert_dfs_equal, mark_as_metamorphic_test


@mark_as_metamorphic_test
def test_concatenation(dfb: DFBuilder.DFBuilder):
    # This only accepts string-only DFs.
    type_check = dfb.check_types(str)
    ret = [dfb.deepcopy()]
    if not type_check:
        # type-check failed, move on
        return ret

    append = "a"

    # Make DF from DFB
    df = dfb.to_df()
    df += append

    # Append to DFB and make DF2
    dfb2 = dfb.map_elements(lambda s: s + "a")
    df2 = dfb2.to_df()

    # f(df(x)) is appending "a" to the df
    # df(f(x)) is appending "a" to each element of the df
    assert_dfs_equal(df, df2, dfb.count_asserts)

    ret.append(dfb2)

    return ret


@mark_as_metamorphic_test
def test_multiplication(dfb: DFBuilder.DFBuilder):
    ret = [dfb.deepcopy()]
    # Make sure this is a multiply-able class.
    if not dfb.check_types((int, float, complex, str)):
        return ret

    # Multiply by 3 and 4.
    for mult in [3, 4]:
        df = dfb.to_df()
        df *= mult

        dfb2 = dfb.map_elements(lambda i: i*mult)
        df2 = dfb2.to_df()

        # f(df(x)) is doing math directly to df
        # df(f(x)) is inserting numbers directly to df
        assert_dfs_equal(df, df2, dfb.count_asserts)

        ret.append(dfb2)
    return ret
