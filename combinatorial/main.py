import pandas as pd


def generate_string_array(start, end):
    result = []
    alphabet_size = ord('Z') - ord('A') + 1
    
    for i in range(start, end):
        quotient, remainder = divmod(i - 1, alphabet_size)
        
        if quotient == 0:
            result.append(chr(remainder + ord('A')))
        else:
            result.append(chr(quotient + ord('A') - 1) + chr(remainder + ord('A')))
    return result

def generate_integer_array(start, end):                             # function that generates a list of integers
    return [i for i in range(start, end)]

def generate_float_array(start, end,):                              # function that generates a list of floats
    return [float(i) for i in range(start, end)]

def generate_array_size(size):                                      # generates a size by size 2D array
    if size <= 0:
        return []
    array = []
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            element = (i - 1) * size + j
            row.append(element)
        array.append(row)
    return array


# Combinatorial Testing - This function works by accepting an argument of 1, 2, or 3. These numbers correspond to the covering array.
def test_system(array_size, index_type, column_type, data_type):    # Note array size, index_type, & column_type need to be the same size. Index, column, and data should be testing different types ints, str, etc.
    # Array size is assigned here. Array sizes are split up in three distinct sizes, small, medium, and large.
    if array_size == 1:                                             # small size 2D array 100 elements
        size = 10                                                   
        array = generate_array_size(size)                           # value to be used in index type etc
    elif array_size == 2:                                           # medium size 2D array 10000 elements
        size = 100
        array = generate_array_size(size) 
    elif array_size == 3:                                           # large size array 1000000 values
        size = 1000
        array = generate_array_size(size) 
    else:
        print("Error, invalid input for array_size")
    
    # Index_type is assigned here. The type is either float, string, or integer. Note that the size must match with the array size above.
    if index_type == 1:                                             # generates an index array with integers                     
        index  = generate_integer_array(0, size)
    elif index_type == 2:
        index = generate_float_array(0, size)                       # generates an index array with floats
    elif index_type == 3:
        index = generate_string_array(0, size)                      # generates an index array with strings
    else: 
        print("Error, invalid input for index_size")

    # Column_type is assigned here. The type is either float, string, or integer. Note that the size must match with the array size above.
    if column_type == 1:                                            # generates an index array with integers                     
        column  = generate_integer_array(0, size)
    elif column_type == 2:
        column = generate_float_array(0, size)                       # generates an index array with floats
    elif column_type == 3:
        column = generate_string_array(0, size)                      # generates an index array with strings
    else: 
        print("Error, invalid input for column_type")

    # Data_type is assigned here
    if data_type == 1:
        data = int
    elif data_type == 2:
        data = float
    elif data_type == 3:
        data = str                           # this currently doesnt work like int and float do
    else:
        print("Error, invalid input for data_type")
        
    return pd.DataFrame(array,index, column, data)                          # output

#*****************Main****************#

test_case = 1
with open("test_case_array.txt") as fo:
    lines = fo.readlines()
    for line in lines:
        values = line.strip().split()
        params = [int(value) for value in values]
        print(f"\nTest case #: {test_case}\nCovering Array Input: {params[0]},{params[1]},{params[2]},{params[3]}\nDataFrame Output:")
        test_case += 1
        print(test_system(params[0],params[1],params[2], params[3]))



 