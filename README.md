# ECE595-OSS-Validation
This GitHub repository shows the programs we used for our OSS Validation Project for ECE 595.

Each folder is intended to be used as a separate Python program. Therefore, to execute the metamorphic testing, the metamorphic program should be treated as its own program and the "main.py" file within the Metamorphic folder should be executed to complete metamorphic testing. Similarly, to execute combinatorial testing, execute Combinatorial/main.py, and to execute Fuzz testing, execute Fuzzing/main.py.

## Next Steps
If we were to continue this project, we could start mixing some of these methods together. For example, we could use combinatorial testing to generate fewer DataFrames in Metamorphic (without significant loss of actual results), allowing us to make more metamorphic tests without requiring significant computation time. We could also mix fuzz testing with metamorphic testing, by applying metamorphic testing to each of the randomly-generated tests provided by the fuzz tester.
