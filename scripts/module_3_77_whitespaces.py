import re
import string

# Function to normalize letter case
def normalizeLetterCase(text):
    # Convert all letters to lowercase
    text = text.lower()
    # Remove unnecessary new line characters
    text = text.replace('\n    \n    \n    ', '').replace(':\n     ', ': ').replace('     ', '')

    list_of_strings = filter(bool, text.split('.'))  # Split the text into sentences

    result = [] # Variable to store the final result
    for sentence in list_of_strings:     # Iterate over each sentence
        first_letter = re.search(r'[a-zA-Z0-9]', sentence).group()  # Find the first non-whitespace character
        # Create a new sentence with an uppercase first letter
        new_sentence = sentence[:sentence.find(first_letter)] + first_letter.capitalize() + sentence[sentence.find(
            first_letter) + 1:]
        result.append(new_sentence) # Add the modified sentence to the result
    result = '.'.join(result)
    return result

# Function to construct a sentence using the last words of each sentence in the original text
def buildSentenceFromLastWords(text):
    split_text = filter(bool, text.split('.'))  # Split the text into sentences
    words_for_sentence = [sentence.split()[-1] for sentence in split_text]  # Extract the last word from each sentence
    sentence = ' '.join(words_for_sentence).capitalize()  # Combine words into a single sentence and capitalize the first letter
    return sentence

# Function to correct the spelling mistake ("iz" -> "is")
def correctSpellingMistake(text):
    # Find occurrences of the standalone word 'iz', surrounded by spaces or special characters, and replace it with 'is'
    updated_text = re.sub(r'([@_!#$%^&*()<>?,/\|}{~:\s])iz([@_!#$%^&*()<>?,/\|}{~:\s])', r'\1is\2', text)
    return updated_text

# Function to calculate the number of whitespace characters in the given text
def calculateWhitespaces(text):
    # Variable to store the count of whitespace characters
    whitespaces_count = 0
    # Check each character in the given text
    for character in text:
        # If the character is a whitespace, increase the counter by 1
        if character in string.whitespace:
            whitespaces_count += 1
    return whitespaces_count

# Main execution block
if __name__ == '__main__':
    # Initial text
    task_string = """homEwork:
     tHis iz your homeWork, copy these Text to variable.
    
    
    
     You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.
    
    
    
     it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
    
    
    
     last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

    # Call previously defined functions
    print(f"\n\033[45mSentence from last words:\033[0m {buildSentenceFromLastWords(normalizeLetterCase(task_string))}.")
    print(f"\n\033[45mText after corrections:\033[0m \n{correctSpellingMistake(normalizeLetterCase(task_string))}.")
    print(f"\n\033[45mNumber of whitespaces:\033[0m {calculateWhitespaces(normalizeLetterCase(task_string))}")