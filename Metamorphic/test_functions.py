import string
import threading
import time

import pandas
from typing import Union

# A bunch of functions used by the other Test-type functions.
# Some of these end up also used by main(), but most of them are used by tests.

asserts_ignored_lock = threading.Lock()
asserts_ignored = 0
asserts_passed_lock = threading.Lock()
asserts_passed = 0

lower_letters = list(string.ascii_lowercase)
upper_letters = list(string.ascii_uppercase)
tests_list = []


# Gets the nth letter of the alphabet
def get_nth_letter(letter_num: int, capital=True):
    if capital:
        letters = string.ascii_uppercase
    else:
        letters = string.ascii_lowercase

    return letters[letter_num - 1]  # cause A would be 0


def get_new_item(input: list, from_list: Union[None, list]=None):
    """
    Tries to generate a value that isn't already in the given input
    Implementation note: It does this the slow way because I wanted to avoid generalization.
    :param input: list or something i can turn into a list()
    :param from_list: If this is None, it'll generate integers. Otherwise, it'll pull from from_list first.
    :return:
    """
    input = list(input)
    i = 0
    while True:
        if from_list is None:
            item = i
        else:
            item = from_list[i] or i

        if item in input:
            i += 1
        else:
            return item


# Checks that two DF's are the same.
def assert_dfs_equal(a: pandas.DataFrame, b: pandas.DataFrame, count_asserts):
    if a.empty and b.empty:
        if count_asserts:
            with asserts_ignored_lock:
                global asserts_ignored
                asserts_ignored += 1
        # print("Ignoring failed assertion - a and b are empty")
        return
    if a.equals(b):
        if count_asserts:
            with asserts_passed_lock:
                global asserts_passed
                asserts_passed += 1
        return
    print("DataFrame A:")
    print(a)
    print("DataFrame B:")
    print(b)
    print("Erroring out.")
    time.sleep(0.1)
    assert False


# Intended to be used as a Python Decorator.
# Adds a test to the list of tests to use.
def mark_as_metamorphic_test(func):
    # print("Marked a metamorphic test.")
    tests_list.append(func)
    return func
