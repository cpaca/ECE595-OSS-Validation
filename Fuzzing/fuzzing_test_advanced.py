import random
import string
import pandas as pd

def generate_random_str(length: int) -> str:
    """Generate a random string of specified length."""
    characters: str = string.ascii_letters + string.digits + string.punctuation
    result_string: str = ''.join(random.choice(characters) for _ in range(length))
    return result_string

def generate_larger_dataframe(num_rows: int) -> pd.DataFrame:
    """Generate a DataFrame with random data."""
    data = {'Name': [], 'Age': [], 'City': []}
    for _ in range(num_rows):
        # Generate random data for each column
        data['Name'].append(generate_random_str(random.randint(5, 20)))
        data['Age'].append(random.randint(20, 60))
        data['City'].append(generate_random_str(random.randint(5, 20)))
    return pd.DataFrame(data)

def fuzzer() -> str:
    """Generator function to yield random strings."""
    while True:
        # Generate a random string of random length
        yield generate_random_str(random.randint(1, 100))

def sample_function(input_str: str, df: pd.DataFrame) -> None:
    """Apply operations to the DataFrame based on the input string."""
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
        elif 'd' in input_str:
            # Attempt to delete a row
            index_to_delete = random.randint(0, len(df) - 1)
            df.drop(index=index_to_delete, inplace=True)
        elif 'f' in input_str:
            # Attempt to fill NaN values with a specific value
            df.fillna(value=0, inplace=True)
        else:
            # Perform a safe operation (do nothing)
            pass
    except Exception as e:
        print('Error:', e)

def export_results_to_file(results: list, file_path: str) -> None:
    """Export results to a text file."""
    with open(file_path, 'w') as file:
        for i, result in enumerate(results, start=1):
            file.write(f'Run #{i}\n')
            file.write(str(result) + '\n')
            file.write("=" * 50 + '\n')

def main():
    # Generate a DataFrame with 5000 rows
    df = generate_larger_dataframe(5000)

    results = []

    # Iterate through the fuzzer and apply operations to the DataFrame
    for i, input_str in enumerate(fuzzer(), start=1):
        # Make a copy of the DataFrame for testing
        df_copy = df.copy()
        
        # Call sample_function with the input string and the DataFrame copy
        sample_function(input_str, df_copy)
        
        # Append the DataFrame copy after applying the operation to results
        results.append(df_copy)

        # Print progress every 100 iterations
        if i % 100 == 0:
            print(f'Completed {i} iterations')

        # Break after 500 iterations
        if i >= 500:
            break

    # Export results to a text file
    export_results_to_file(results, 'results.txt')

if __name__ == '__main__':
    main()
