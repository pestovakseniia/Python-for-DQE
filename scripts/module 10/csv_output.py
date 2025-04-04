import re
import csv

def generate_csv_file_1(input_file_name, csv_name):
    """Function that generates CSV file for words and their count"""

    # Read the source file and split it into words (all words are preprocessed in lowercase)
    with open(input_file_name, 'r', encoding='utf-8-sig') as file:
        words_list = re.split(r'[ \n`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', file.read().lower())

    # Create an empty dictionary and populate it with words and their count
    dictionary_of_words = {}
    for word in words_list:
        if word.isalpha():  # If it is a word, not a date, then include it in dictionary
            dictionary_of_words[word] = dictionary_of_words.get(word, 0) + 1

    # This block generates a CSV file with headers based on dictionary_of_words
    headers = ["Слово", "Количество"]
    with open(csv_name, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=headers)   # Create a DictWriter object
        writer.writeheader()  # Write header row
        for key,value in dictionary_of_words.items():
            writer.writerow({"Слово": key, "Количество": value})  # Write data rows

def generate_csv_file_2(input_file_name, csv_name):
    """ Function that generates CSV file for letters and their count"""

    # Read the source file and split it into words (all words are preprocessed as-is - lowercase and uppercase)
    with open(input_file_name, 'r', encoding='utf-8-sig') as file:
        words_list = re.split(r'[ \n`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', file.read())

    # Create an empty dictionary and populate it with letters and their count
    dictionary_of_letters = {}
    for word in words_list: # Iterate over each word in a list of words
        if word.isalpha():  # If it is a word, not a date, then further process it
            for letter in word: # Iterate over each letter in a word
                if letter.lower() not in dictionary_of_letters: # If a letter does not exit in a dictionary yet, then add it
                    dictionary_of_letters[letter.lower()] = [1, 0]
                else:                                            # If a letter already exits in a dictionary, then increase 'Count_all'
                    dictionary_of_letters[letter.lower()][0] += 1
                if letter.isupper():                            # If a letter is of uppercase, then increase 'Count_uppercase'
                    dictionary_of_letters[letter.lower()][1] += 1

    # Block that calculates all letters in a dictionary and writes down 'Percentage' for each letter
    all_letters_total = sum([value[0] for value in dictionary_of_letters.values()])
    for key, value in dictionary_of_letters.items():
        value.append(round(value[0] / all_letters_total * 100, 2))

    # This block generates a CSV file with headers based on dictionary_of_letters
    headers = ["Letter", "Count_all", "Count_uppercase", "Percentage"]
    with open(csv_name, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for key,value in dictionary_of_letters.items():
            writer.writerow({"Letter": key, "Count_all": value[0], "Count_uppercase": value[1], "Percentage": value[2]})