# Tests related to manipulating the size or shape of the dataframe
import DFBuilder
from test_functions import assert_dfs_equal, mark_as_metamorphic_test


@mark_as_metamorphic_test
def test_add_str_columns(dfb: DFBuilder.DFBuilder):
    return test_add_columns(dfb, [2, 3, 5, "B", "C"])


def test_add_columns(dfb: DFBuilder.DFBuilder, new_col_names):
    new_dfbs = [dfb.deepcopy()]
    for new_col_name in new_col_names:
        # Generate information for new column
        new_col_contents = [new_col_name * j for j in range(1, 1+dfb.height())]
        if isinstance(new_col_name, str):
            new_col_contents = [s.lower() for s in new_col_contents]

        # This is how we add the new column to the DF
        df = dfb.to_df()
        if new_col_name in df:
            # Can't have two columns with the same name.
            # print("Skipping column")
            continue
        # noinspection PyTypeChecker
        df.insert(df.shape[1], new_col_name, new_col_contents)

        # Add column to DFB and generate df from that
        dfb.data_dict[new_col_name] = {df.index[i]: new_col_contents[i] for i in range(len(new_col_contents))}
        df2 = dfb.to_df()

        # f(df(x)) is new column to df
        # df(f(x)) is new column to dict, which becomes df
        assert_dfs_equal(df, df2, dfb.count_asserts)

        # Asserts complete, update:
        new_dfbs.append(dfb.deepcopy())

    return new_dfbs


# Note: While this test attempts to delete every column once,
# it doesn't save every DF. Otherwise, later tests will start running
# millions of very-similar tests very fast. Or, rather, very slow.
@mark_as_metamorphic_test
def test_delete_columns(dfb: DFBuilder.DFBuilder):
    new_dfbs = [dfb.deepcopy()]
    col_names = dfb.col_names()

    for i in range(len(col_names)):
        col_name = col_names[i]

        # First, make a DF and delete the relevant column
        df = dfb.to_df()
        del df[col_name]

        # Then delete the relevant column from DFB
        dfb2 = dfb.filter_cols(lambda name, data: name != col_name)
        df2 = dfb2.to_df()

        assert_dfs_equal(df, df2, dfb.count_asserts)

    return new_dfbs


# Unlike test_delete_columns, I opted to have this one create more tests due to the lack of variation
# in tests & how many rows they have.
@mark_as_metamorphic_test
def test_delete_rows(dfb: DFBuilder.DFBuilder):
    dfb = dfb.deepcopy()
    new_dfbs = [dfb.deepcopy()]
    row_names = dfb.row_names()

    for row_name in row_names:
        # make the df and drop the row from the df
        df = dfb.to_df()
        df = df.drop(row_name)

        dfb2 = dfb.map_cols(lambda col_name, data: {key: data[key] for key in data if key != row_name})
        df2 = dfb2.to_df()

        # f(df(x)) drops the row directly from df
        # df(f(x)) drops the row from the data then makes a df
        assert_dfs_equal(df, df2, dfb.count_asserts)

        new_dfbs.append(dfb2.deepcopy())

    return new_dfbs
