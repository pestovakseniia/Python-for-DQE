import datetime
import text_formatting
import json
import xml.etree.ElementTree as ET
import re


# Class for News object
class News:
    # Init method to initialize 'text' and 'city' parameters during an instance creation
    def __init__(self, text, city):
        self.text = text
        self.city = city

    # Function to form a news text
    def formNews(self):
        result = f"\nНовости -------------------------\n{self.text}\n{self.city}, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
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
        result = f"\nРеклама -------------------\n{self.text}\nДействительна до: {self.expiration_date}, {self.__calculateDaysLeft()} дней осталось\n"
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
        result = f"\nГороскоп --------------------\n{self.text}\nТэги: {self.__generateEmojis()}\n"
        return result


# Class for provisioning input as a json-file
class TextExporterJson:
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
                    dictionary_with_normalized_case[key] = text_formatting.normalizeLetterCase(object[key])
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


# Class for provisioning input as a xml-file
class TextExporterXml:
    def __init__(self, source_file):
        self.source_file = source_file
        self.tree = ET.parse(source_file)
        self.root = self.tree.getroot()

    def formObjects(self):
        result = ''
        for record in self.root:
            if record[0].text == 'News':
                single_news = News(record[1].text, record[2].text)
                result = result + single_news.formNews()
            elif record[0].text == 'PrivateAd':
                single_private_ad = PrivateAd(record[1].text, record[2].text)
                result = result + single_private_ad.formPrivateAd()
            elif record[0].text == 'Horoscope':
                single_horoscope = Horoscope(record[1].text)
                result = result + single_horoscope.formHoroscope()
        return result
