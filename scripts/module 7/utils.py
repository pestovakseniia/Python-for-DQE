import os
import datetime
import exceptions

# Function to check if an input string is empty
def checkUserInput(text):
    if text.strip() == "":
        raise exceptions.EmptyInput


# Function to check if a file in a specified directory exists
def checkFilePath(file_path):
    if not os.path.isfile(file_path):
        raise exceptions.InvalidFilePath

# Function to check if an input date is in past
def checkDate(datetime_variable: str):
    datetime_variable = datetime.datetime.strptime(datetime_variable, "%Y-%m-%d").date()
    if datetime_variable < datetime.datetime.now().date():
        raise exceptions.InvalidDate