import datetime
import re
import os
import module_3
import json


# Custom exception class for handling invalid input source (i.e., not in (1, 2, й/q))
class InvalidInputSource(Exception):
    def __init__(self, message='Введен неверный формат источника ввода. Попробуй снова'):
        self.message = message
        super().__init__(self.message)


# Custom exception class for handling invalid publish type (i.e., not in (1, 2, 3))
class InvalidPublishType(Exception):
    def __init__(self, message='Введен неверный формат типа публикации. Попробуй снова'):
        self.message = message
        super().__init__(self.message)


# Custom exception class for handling invalid dates (date in the past)
class InvalidDate(Exception):
    def __init__(self, message='Введена дата в прошлом. Измени дату'):
        self.message = message
        super().__init__(self.message)


# Custom exception for handling invalid input (empty string)
class EmptyInput(Exception):
    def __init__(self, message='Введена пустая строка. Попробуй снова'):
        self.message = message
        super().__init__(self.message)


# Custom exception for handling invalid file path
class InvalidFilePath(Exception):
    def __init__(self, message='Файла по указанному пути не существует. Попробуй снова'):
        self.message = message
        super().__init__(self.message)


# Class for News object
class News:
    # Init method to initialize 'text' and 'city' parameters during an instance creation
    def __init__(self, text, city):
        self.text = text
        self.city = city

    # Function to form a news text
    def formNews(self):
        result = f"\nNews -------------------------\n{self.text}\n{self.city}, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        return result


# Class for Private Ad object
class PrivateAd:
    # Init method to initialize 'text' and 'expiration date' parameters during an instance creation
    def __init__(self, text, expiration_date: str):
        self.text = text
        # Parse a string into a datetime object for future calculations
        self.expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()

    # Private method for calculating days left til ad expiration
    def __calculateDaysLeft(self):
        self.days_left = (self.expiration_date - datetime.datetime.now().date()).days
        return self.days_left

    # Function to form a private ad text
    def formPrivateAd(self):
        result = f"\nPrivate Ad -------------------\n{self.text}\nActual until: {self.expiration_date}, {self.__calculateDaysLeft()} days left\n"
        return result


# Class for Horoscope object
class Horoscope:
    def __init__(self, text):
        self.text = text

    # Private method to define tags from an initial text
    def __generateEmojis(self):
        # Dictionary of available tags
        emojis_dictionary = {"козерог": "♑", "водолей": "♒", "рыбы": "♓", "овен": "♈", "телец": "♉", "близнецы": "♊",
                             "рак": "♋", "лев": "♌", "дева": "♍", "весы": "♎", "скорпион": "♏", "стрелец": "♐",
                             "хорошо": "🔆", "отлично": "🚀", "плохо": "☃️", "замечательно": "✨"}
        # split initial text into multiple words
        emojis_dictionary_split = re.split(r'[ `\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', self.text.lower())
        tags = []  # List to store the resulting tags

        # Loop to iterate over each word in initial text
        for word in emojis_dictionary_split:
            # if a word is present in the dictionary of available tags, then add the tag to the resulting tags list
            if word in emojis_dictionary:
                tags.append(emojis_dictionary[word])

        tags_unitied = ''.join(tags)
        return tags_unitied

    # Function to form a Horoscope text
    def formHoroscope(self):
        result = f"\nHoroscope --------------------\n{self.text}\nTags: {self.__generateEmojis()}\n"
        return result


# Class for provisioning input as a file
class TextExporter:
    def __init__(self, source_file):
        self.source_file = source_file
        with open(source_file, 'r', encoding='utf-8') as file:  # read a source file
            text_as_json = file.read()
        # Parse a source file as json file and assign a class's variable text with the resulting dictionary
        self.text = json.loads(text_as_json)
        self.__normalizeLetterCase()

    # Private method to normalize letters case in a source file
    def __normalizeLetterCase(self):
        text_with_normalized_case = []
        for object in self.text:
            dictionary_with_normalized_case = {}
            for key, value in object.items():
                if key in ('text', 'city'):
                    dictionary_with_normalized_case[key] = module_3.normalizeLetterCase(object[key])
                else:
                    dictionary_with_normalized_case[key] = value
            text_with_normalized_case.append(dictionary_with_normalized_case)
        self.text = text_with_normalized_case

    # Method to form text out of all input objects
    def formObjects(self):
        result = ''
        for object in self.text:
            if object['type'] == 'News':
                single_news = News(object['text'], object['city'])
                result = result + single_news.formNews()
            elif object['type'] == 'PrivateAd':
                single_private_ad = PrivateAd(object['text'], object['expiration_date'])
                result = result + single_private_ad.formPrivateAd()
            elif object['type'] == 'Horoscope':
                single_horoscope = Horoscope(object['text'])
                result = result + single_horoscope.formHoroscope()
        return result

    # Method to delete a source file
    def removeSourceFile(self):
        os.remove(self.source_file)

# Function to check if an input string is empty
def checkUserInput(text):
    if text.strip() == "":
        raise EmptyInput


# Function to check if a file in a specified directory exists
def checkFilePath(file_path):
    if not os.path.isfile(file_path):
        raise InvalidFilePath

# Function to check if an input date is in past
def checkDate(datetime_variable: str):
    datetime_variable = datetime.datetime.strptime(datetime_variable, "%Y-%m-%d").date()
    if datetime_variable < datetime.datetime.now().date():
        raise InvalidDate


# Main part
if __name__ == '__main__':
    # Open a file for both writing and reading
    with open('results.txt', 'a+', encoding='utf-8') as file:
        file.seek(0)
        # Condition to check if a file is empty. If it is, then write a string (written only once)
        if file.read().strip() == "":
            file.write("News feed: ")

        while True:
            try:
                inputSource = input(
                    'Хочешь ввести информацию ч/з консоль или через файл: 1 - консоль, 2 - файл, й/q - завершить? ')
                if inputSource == '1':
                    publishType = input('Что хочешь опубликовать: 1 - новость, 2 - рекламу, 3 - гороскоп? ')
                    if publishType == '1':
                        newsText = input('Введи ТЕКСТ новости: ')
                        checkUserInput(newsText)

                        newsCity = input('Введи ГОРОД: ')
                        checkUserInput(newsCity)

                        pieceOfNews = News(newsText, newsCity)  # Instance creation of News class
                        file.write(pieceOfNews.formNews())
                    elif publishType == '2':
                        adText = input('Введи ТЕКСТ рекламы: ')
                        checkUserInput(adText)

                        adValidUntil = input('Введи ДАТУ, по которую будет опубликована реклама (yyyy-mm-dd): ')
                        checkUserInput(adValidUntil)
                        checkDate(adValidUntil)

                        pieceOfPrivateAd = PrivateAd(adText, adValidUntil)  # Instance creation of PrivateAd class
                        file.write(pieceOfPrivateAd.formPrivateAd())
                    elif publishType == '3':
                        horoscopeText = input('Введи ТЕКСТ гороскопа: ')
                        checkUserInput(horoscopeText)

                        pieceOfHoroscope = Horoscope(horoscopeText) # Instance creation of Horoscope class
                        file.write(pieceOfHoroscope.formHoroscope())
                    else:
                        raise InvalidPublishType
                elif inputSource == '2':
                    userDirectory = input('Введите ПУТЬ к файлу с данными: ') or 'module_6_input.json'
                    checkFilePath(userDirectory)

                    dataToExport = TextExporter(userDirectory)
                    file.write(dataToExport.formObjects())
                    dataToExport.removeSourceFile()
                elif inputSource in ('й', 'q'):
                    break
                else:
                    raise InvalidInputSource
            except InvalidInputSource as error:
                print(f'\033[31m{error}\033[0m')
            except InvalidPublishType as error:
                print(f'\033[31m{error}\033[0m')
            except InvalidDate as error:
                print(f'\033[31m{error}\033[0m')
            except EmptyInput as error:
                print(f'\033[31m{error}\033[0m')
            except InvalidFilePath as error:
                print(f'\033[31m{error}\033[0m')