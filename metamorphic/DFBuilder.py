from typing import Union, Type

import pandas
import copy


# Theoretically has all of the elements needed to generate a DF.
# WARNING: This will produce INCORRECT RESULTS if the target DF is an empty DF!
class DFBuilder:
    def __init__(self):
        self.data_dict: dict[dict] = None
        self._initialized: bool = False
        self.count_asserts: bool = False

    def self_check(self):
        if not self._initialized:
            raise RuntimeError("Don't use DFBuilder's Initializer! Use from_df instead!")

    @staticmethod
    def from_df(df: pandas.DataFrame):
        out = DFBuilder()
        out.data_dict = df.to_dict()
        out._initialized = True
        return out

    def to_df(self) -> pandas.DataFrame:
        self.self_check()
        return pandas.DataFrame(self.data_dict)

    def deepcopy(self):
        newDFB = DFBuilder()
        self.self_check()

        newDFB.data_dict = copy.deepcopy(self.data_dict)
        newDFB._initialized = self._initialized

        return newDFB

    def col_names(self):
        self.self_check()
        out = list(self.data_dict.keys())
        return out

    def num_cols(self):
        return len(self.col_names())

    # This assumes all of the columns have all of the rows
    # but if this is a well-formed DF that'll be true anyway
    # and if it's not a well-formed DF, to_df() will crash (I think)
    def row_names(self):
        self.self_check()
        # Get a column
        col: dict = next(iter(self.data_dict.values()))
        # its keys are the row names
        row_names = col.keys()
        return row_names

    def height(self):
        self.self_check()
        # First, we need to get a column. Shouldn't matter which column if this is a valid DF.
        col = next(iter(self.data_dict.values()))
        # Its height will be the number of elements it has
        return len(col)

    def get_types(self):
        self.self_check()
        # Gets the list of types in this DF.
        # I think df.dtypes could do this too? But it goes to dtype() instead of giving me python types...
        out = set()
        for col in self.data_dict.values():
            for item in col.values():
                item_type = type(item)
                out.add(item_type)
        return out

    def check_types(self, types: Union[type, tuple[Type, ...]]):
        if isinstance(types, type):
            types = (types, )

        self_types = self.get_types()
        assert len(self_types) > 0
        for self_type in self_types:
            if isinstance(self_type, types) or (any(self_type == A for A in types)):
                # this self-type is valid, move on
                pass
            else:
                return False
        # no invalid self-types found
        return True

    # Applies map(x) to every element of dict. treats it kinda like a 2d array lol
    def map_elements(self, mapper):
        self.self_check()

        out_dict = copy.deepcopy(self.data_dict)
        for col_name in out_dict:
            col = out_dict[col_name]
            for idx in col:
                col[idx] = mapper(col[idx])
            out_dict[col_name] = col

        out_dfb = DFBuilder()
        out_dfb.data_dict = out_dict
        out_dfb._initialized = self._initialized

        return out_dfb

    # Applies map(col_name, col) to every column of dict
    def map_cols(self, mapper):
        self.self_check()

        out_dict = {}
        for col_name in self.data_dict:
            col = self.data_dict[col_name]
            out_dict[col_name] = mapper(col_name, col)

        out_dfb = DFBuilder()
        out_dfb.data_dict = out_dict
        out_dfb._initialized = self._initialized

        # easiest way to check this is still a valid DFB
        out_dfb.to_df()

        return out_dfb

    # Applies filter(col_name, col) to every column of dict.
    def filter_cols(self, filterer):
        self.self_check()

        out_dict = {}
        for col_name in self.data_dict:
            col = self.data_dict[col_name]
            if filterer(col_name, col):
                out_dict[col_name] = col

        out_dfb = DFBuilder()
        out_dfb.data_dict = out_dict
        out_dfb._initialized = self._initialized

        return out_dfb

