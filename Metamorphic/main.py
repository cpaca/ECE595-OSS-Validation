import importlib
import pathlib
import time

import numpy
import pandas
import threading
import queue

import test_functions
# from tests import df_tests, string_tests, number_tests

import DFBuilder

queue_lock = threading.Lock()
tasks = queue.Queue()
# Don't set this above 1.
# I've done some framework for multithreading, but the
# counters keep giving me incorrect values.
NUM_THREADS = 1


# This function runs in two ways:
# First, it runs through every test with the root DFBs, then uses the return value (multiple DFBs) to create more tests.
# So it takes the 1 root DFB, the 1st test makes it into 6 DFBs for 6 tasks, the next test makes it into more DFBs,
# etc.
# aka 1 root DFB -> many test DFBs (currently 188 test DFBs made)
#
# Second, now that it has used all of the tests to make many DFBs,
# it runs every test again, using the full set of the newly-constructed DFBs.
# (The second time around, it doesn't construct an even larger set of more DFBs,
# as many of them would very similar/identical to
def run_tests():
    while True:
        task = tasks.get()
        dfb: DFBuilder.DFBuilder = task["dfb"]

        test_num: int = task["test_num"]
        num_tests = len(test_functions.tests_list)
        if test_num >= 2 * num_tests:
            # Third time around:
            # Don't do anything for the third time around, just end.
            # okay, fine, put it back onto the queue so the task counter is accurate
            tasks.put(task)
            return
        elif test_num >= 1 * num_tests:
            # Second time around:
            # Don't make new tests, but actually count the asserts this time.
            create_new_DFBs = False
            dfb.count_asserts = True
        elif test_num >= 0 * num_tests:
            # First time around:
            # Create new tests, but don't count the asserts so as to not double-count with 2nd time around.
            create_new_DFBs = True
            dfb.count_asserts = False
        else:
            assert False

        # Clamping for the 2nd time around.
        test_num = test_num % num_tests

        test = test_functions.tests_list[test_num]
        new_dfbs = test(dfb)
        if not create_new_DFBs:
            # don't create new DFBs, but transfer this DFB over to the next one.
            new_dfbs = [dfb.deepcopy()]
        if new_dfbs is None:
            continue
        for i in range(len(new_dfbs)):
            new_dfb = new_dfbs[i]
            new_task = {
                "name": task["name"] + str(i) + "-",
                "dfb": new_dfb.deepcopy(),
                "test_num": task["test_num"] + 1
            }
            tasks.put(new_task)


def add_root_task(name, data):
    task = {
        "name": name,
        "dfb": DFBuilder.DFBuilder.from_df(pandas.DataFrame(data)),
        "test_num": 0
    }
    tasks.put(task)


def load_tests():
    # Loading tests is now done using a decorator on each function.
    # Therefore, if we just import each file, all decorators
    # will activate, and all functions will add themselves to the test_list.
    # All tests are in the file tests, so just import all of those.
    tests_folder = pathlib.Path(__file__).parent.joinpath("tests")
    print("Importing all files in folder", tests_folder)
    for filepath in tests_folder.iterdir():
        filename = filepath.name
        if not filename.endswith(".py"):
            # Probably pycache.
            continue
        # The [:-3] gets rid of the .py
        module_name = "tests." + filename[:-3]
        importlib.import_module(module_name)
    print("Import complete.")


if __name__ == "__main__":
    data = {"A": ["a", "aa", "null\0"]}
    add_root_task("str1-", data)

    data = {1: [0, 1, -2.5], 4: [numpy.nan, numpy.nan, numpy.nan], 59: [-7.983, 41.43, numpy.nan]}
    add_root_task("int1-", data)

    load_tests()

    thread_list = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=run_tests, )
        thread.start()
        thread_list.append(thread)

    print(f"Created {NUM_THREADS} threads.")

    for thread in thread_list:
        thread.join()

    print("\nMetamorphic testing complete.")
    print("Asserts completed:", test_functions.asserts_passed)
    print("Failed asserts ignored:", test_functions.asserts_ignored)
    print("Tasks in tasks variable:", tasks.qsize())
    # print("Tests ran:", tests.asserts_passed)

