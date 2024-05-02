# Pandas DataFrame Fuzzing Test

This Python script generates random operations on a pandas DataFrame to test various functionalities and error handling through fuzzing tests.

## Description

The script performs the following tasks:

- Generates a larger pandas DataFrame with random data.
- Uses a fuzzer to generate random input strings.
- Applies random operations on the DataFrame based on the input strings.
- Prints the DataFrame after each operation.

## File Structure

- `fuzzing_tests.py`: Python script containing simpler iteration of fuzzing tests.
-  `fuzzing_test_advanced.py`: Python Script containing advanced iterations of fuzzing tests with larger DataFrames and operations.
-  `results.txt`: This file provides sample results after running the 'fuzzing_test_advanced.py' for 500 iterations
- `README.md`: This file, providing an overview of the project.



