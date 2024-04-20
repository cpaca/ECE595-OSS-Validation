import random
import string
import pandas as pd

def generate_random_str(length:int) -> str:
    characters: str = string.ascii_letters + string.digits + string.punctuation
    result_string: str = ''.join(random.choice(characters) for _ in range(length))
    return result_string

def fuzzer() -> str:
    while True:
        yield generate_random_str(random.randint(1, 100))

def sample_function(input_str: str, df: pd.DataFrame) -> None:
    try:
        if 'a' in input_str:
            # Attempt to add a row to the DataFrame
            row_data = {'Name': 'John', 'Age': 25, 'City': 'Boston'}
            df.loc[len(df)] = row_data
        elif 'dr' in input_str:
            # Attempt to drop a column from the DataFrame
            df.drop(columns=['City'], inplace=True)
        elif 'un' in input_str:
            # Attempt to perform an unsupported operation on the DataFrame
            df = df.some_unsupported_operation()
        elif 'm' in input_str:
            # Attempt to modify age column (adding 5 to all ages)
            df['Age'] = df['Age'] + 5
        elif 'sor' in input_str:
            # Attempt to sort the DataFrame by age
            df.sort_values(by='Age', inplace=True)
        elif 'reset' in input_str:
            # Attempt to reset the index of the DataFrame
            df.reset_index(drop=True, inplace=True)
        else:
            # Perform a safe operation (do nothing)
            pass
    except Exception as e:
        print('Error:', e)

def main():
    # Creating DataFrame from lists
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']}
    df = pd.DataFrame(data)

    for i, input_str in enumerate(fuzzer(), start=1):
        print(f'Run #{i}')
        print("Input:", input_str)
        
        # Make a copy of the DataFrame for testing
        df_copy = df.copy()
        
        # Call sample_function with the input string and the DataFrame copy
        sample_function(input_str, df_copy)
        
        # Print the DataFrame copy after applying the operation
        print("DataFrame after operation:")
        print(df_copy)
        print("=" * 50)
        if i >= 100:
            break

if __name__ == '__main__':
    main()
