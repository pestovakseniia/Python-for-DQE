import datetime
import text_formatting
import json
import xml.etree.ElementTree as ET
import re
import pyodbc
import db_schema as sch


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
        self.tags = self.__generateEmojis()

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

        self.tags_unitied = ''.join(tags)
        return self.tags_unitied

    # Function to form a Horoscope text
    def formHoroscope(self):
        result = f"\nГороскоп --------------------\n{self.text}\nТэги: {self.tags}\n"
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


class DBConnection:
    def __init__(self, server_name, port_number, db_name, user, password):
        self.connection = pyodbc.connect(
            "DRIVER={PostgreSQL Unicode};"
            f"SERVER={server_name};"
            f"PORT={port_number};"
            f"DATABASE={db_name};"
            f"UID={user};"
            f"PWD={password};"
        )
        if self.connection is not None:
            print(f"\033[32mConnection to PostgreSQL.{db_name} established.\033[0m")
        self.cursor = self.connection.cursor()

    # Method to be used inside ContextManager for setting up
    def __enter__(self):
        return self

    # Method to be used inside ContextManager for closing connection
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        print("\033[32mConnection to PostgreSQL closed.\033[0m")

    def __checkDups(self, table_name, *args):
        self.cursor.execute(f"SELECT * FROM {table_name} "
                         f"WHERE text = '{args[0]}' "
                         f"AND {list(sch.SCHEMA[table_name].keys())[1]} = '{args[1]}'")
        return self.cursor.fetchall()

    def insert_single_record(self, table_name, *args):
        attributes = ", ".join(f"{key} {value}" for key, value in sch.SCHEMA[table_name].items())
        columns = ", ".join(f"{key}" for key in sch.SCHEMA[table_name].keys())

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({attributes})")

        if self.__checkDups(table_name, *args) == []:
            self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES {args}")
        else:
            print(f"\033[31mRecord with '{args[0]}', '{args[1]}' is duplicate -> NOT INSERTED\033[0m")
        self.cursor.commit()

    def insert_from_json(self, TextExporterJsonObject):
        """Inserts a record or multiple records into a database from a json file. """
        data = TextExporterJsonObject.text
        for row in data:
            self.insert_single_record(row['type'], row['text'], list(row.values())[2] if row['type'] != 'Horoscope' else Horoscope(row['text']).tags)

    def insert_from_xml(self, TextExporterXmlObject):
        """Inserts a record or multiple records into a database from a xml file. """
        for row in TextExporterXmlObject.root:
            self.insert_single_record(row[0].text, row[1].text,
                                      row[2].text if row[0].text != 'Horoscope' else Horoscope(row[1].text).tags)