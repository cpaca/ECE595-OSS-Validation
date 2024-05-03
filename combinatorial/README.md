# Pandas DataFrame Combinatorial Test
This Python script conducts combinatorial testing on a Pandas DataFrame by utilizing a covering array text file to execute multiple test cases automatically. Combinatorial testing aims to identify software bugs stemming from combinations of input parameters, ensuring comprehensive testing coverage.

## Method
main.py imports "test_case_array.txt" to load a test case to be run. Test case data is passed to test_system where DataFrame output is returned. This output is printed where the user can review to check if the DataFrame output is valid.

## File data
### main.py
The main body code that imports the covering array and runs the test_system() function. In each iteration of the loop, it retrieves a test case and feeds its data into test_system(). Additionally, it displays the output of test_system(), along with the test number and the inputs of each test case, until all test cases have been executed. Subsequently, the test case outputs can be manually reviewed in the terminal.

### test_system(array_size, index_type, column_type, data_type)
This function works by accepting an integer of (1,2, or 3) for each parameter. Each integer represents a trait that describes a particular test case. Each test case can be represented by a sequence of integers such as 1, 1, 1, 1 (test case 1). The code works by checking the integer value passed to each parameter and assigning appropriate values to variables "array", "index", "column", and "data". These variables are then passed to DataFrame and the DataFrame output is returned.

### README.md
README.md is this file, and summarizes how the program executes. It is not used in program execution, and deleting this file does not affect the output of the program.
