# Pandas DataFrame Metamorphic Tests
This Python program performs metamorphic-style testing on the Pandas DataFrame to test that manipulating the DataFrame is equivalent to manipulating its internal data directly.

## Method
main.py imports every file in Metamorphic/tests to get a list of tests to run. Then, for every test:
- Stage 1 uses root data + all tests to construct test data.
- Stage 2 uses test data + all tests to count number of passed asserts.

### Stage 1
The program starts with two basic sets of data. For each test:
1. Select some data, which is represented as an unbuilt DataFrame.
2. Run the test. Do NOT count assertions.
3. The test will construct an additional (or multiple additional) unbuilt DataFrames. Metamorphic testing compares f(x') and (f(x))', these additional unbuilt dataframes can be thought of as x'.
4. Repeat steps 1-3 with all basic sets of data.
5. Collect all additional unbuilt DataFrames. (For example, a test which creates abs(x) may turn 2 basic dataframes into 4 basic dataframes.)
6. Repeat steps 1-5 for all tests, using the new set of unbuilt DataFrames

Stage 1 is complete when steps 6 is complete and has executed on all tests.
### Stage 2
The program now has a large set of unbuilt DataFrames from step 1. (Currently, this is a set of 746 unbuilt DataFrames; that number can change wildly as tests are added or modified.)
Stage 2 is as follows:
1. Select a test.
2. Select an unbuilt DataFrame.
3. Run the test with the unbuilt DataFrame. DO count assertions. (Note that the test may sometimes choose to report numbers besides 1 assertion executed, such as 0 assertions executed if it doesn't make sense to test or 5 assertions executed if multiple simialr tests are in one function.)
4. Repeat steps 2-3 with all (currently 746) unbuilt DataFrames.
5. Repeat steps 1-4 with all tests collected from tests directory.

Stage 2 is complete (and the program outputs its report) after step 5 has completed with all tests.
## File data
### main.py
The primary code for stages 1 and 2 are in main.py. However, the other files store common functions.
### DFBuilder.py
Unbuilt DataFrames are stored in DFBuilder, which is similar to DataFrame but was constructed without looking at DataFrame's implementation and is missing many of the functionalities of DataFrame. This means it is closer to "raw data" - ie, an unbuilt DataFrame - than it is to the actual DataFrame.
### test_functions.py
test_functions stores some functions common to multiple tests but not used outside of those. The most important of those are assert_dfs_equal, which performs the assertion and also increments the assertion count, as well as mark_as_metamorphic_test, which adds a test to the list of tests to execute.
### README.md
README.md is this file, and summarizes how the program executes. It is not used in program execution, and deleting this file does not affect the output of the program.
