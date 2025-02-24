# 1. create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

# 2. get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
# Each line of code should be commented with description.

# Import a module to work with random numbers
import random

# Function that generates a list of dictionaries based on task requirements
def generateListOfDictionaries() -> list:
    # Initialize an empty list to store the resulting dictionaries
    list_of_dicts = []
    # Outer loop to iterate over the total number of dictionaries in the list
    for i in range(random.randint(2, 10)):
        inner_dict = {}
        # Inner loop to iterate over the number of items in a single dictionary
        for n in range(random.randint(2, 10)):
            random_key = chr(random.randint(ord('a'), ord('z')))    # Generate a random key consisting of lowercase letters
            random_value = random.randint(0, 100)   # Generate a random value consisting of numbers from 0 to 100
            inner_dict[random_key] = random_value   # Add a key-value pair to the current dictionary
        list_of_dicts.append(inner_dict)    # Add the generated dictionary to the list

    return list_of_dicts

def createDictionaryOfMaxValues(list_of_dicts) -> dict:
    max_values = {} # Dictionary that stores keys and their maximum values across all dictionaries
    occurrences_count = {}  # Dictionary that tracks the occurrence count of each key across all dictionaries
    dict_index = {} # Dictionary that records the index of the dictionary where the maximum value was found
    # Outer loop to iterate over the total number of dictionaries in the list
    for index, dictionary in enumerate(list_of_dicts, start=1):
        # Inner loop to iterate over the number of items in a single dictionary
        for key, value in dictionary.items():
            # Update the key occurrence dictionary in all cases
            occurrences_count[key] = occurrences_count.get(key, 0) + 1
            # If a key is not yet present in the dictionary of max values OR if its current value is lower than
            # another value, then update the max value and record the index of the dictionary where the new max
            # value was found
            if key not in max_values or value > max_values[key]:
                max_values[key] = value
                dict_index[key] = index

    # This block consolidates the results obtained in the previous step
    result = {}
    # Loop to iterate over the max_values dictionary
    for key, value in max_values.items():
        # If a key appeared only once, add it to the final dictionary with its max value
        if occurrences_count[key] == 1:
            result[key] = value
        # If a key appeared multiple times, add it to the final dictionary with an index
        # indicating the dictionary where the max value was found, along with its max value
        else:
            result[f"{key}_{dict_index[key]}"] = value
    return result

# Main part of the program
if __name__ == '__main__':
    my_list = generateListOfDictionaries()  # Call a function to generate a list of dictionaries
    my_dict = createDictionaryOfMaxValues(my_list) # Call a function to generate a dictionary of maximum values

    # Print the result of the generateListOfDictionaries function
    print('List of dictionaries:')
    for index, dictionary in enumerate(my_list, start=1):
        print(f"({index}) {dictionary}")

    # Print the result of the createDictionaryOfMaxValues function
    print(f'\nDictionary of max values: \n{my_dict}')