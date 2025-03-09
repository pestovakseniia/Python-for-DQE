import datetime
import re


# Custom exception class for handling invalid publish type
class InvalidPublishType(Exception):
    def __init__(self, message='Введен неверный формат типа публикации. Попробуй снова'):
        self.message = message
        super().__init__(self.message)


# Custom exception class for handling invalid dates
class InvalidDate(Exception):
    def __init__(self, message='Введена дата в прошлом. Измени дату'):
        self.message = message
        super().__init__(self.message)


# Class for News object
class News:
    # Init method to initialize 'text' and 'city' parameters during an instance creation
    def __init__(self, text, city):
        self.text = text
        self.city = city

    # Function to print a piece of news
    def printNews(self):
        result = f"\nNews -------------------------\n{self.text}\n{self.city}, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        return result


# Class for Private Ad object
class PrivateAd:
    # Init method to initialize 'text' and 'expiration date' parameters during an instance creation
    def __init__(self, text, expiration_date):
        self.text = text
        self.expiration_date = expiration_date

    # Private method for calculating days left til ad expiration
    def __calculateDaysLeft(self):
        self.days_left = (self.expiration_date - datetime.datetime.now().date()).days
        return self.days_left

    # Function to print a private ad
    def printPrivateAd(self):
        result = f"\nPrivate Ad -------------------\n{self.text}\nActual until: {self.expiration_date}, {self.__calculateDaysLeft()} days left\n"
        return result


# Class for Horoscope object
class HoroscopeOfTheDay:
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

    # Function to print a Horoscope
    def printHoroscopeOfTheDay(self):
        result = f"\nHoroscope --------------------\n{self.text}\nTags: {self.__generateEmojis()}\n"
        return result


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
                publishType = input('Что хочешь опубликовать: 1 - новость, 2 - рекламу, 3 - гороскоп, й - завершить? ')
                if publishType == '1':
                    newsText = input('Введи ТЕКСТ новости: ') or 'Что-то новое случилось'
                    newsCity = input('Введи ГОРОД: ') or 'Батуми'

                    # Instance creation of News class
                    pieceOfNews = News(newsText, newsCity)
                    # A printNews function call, then the result recording to a file
                    file.write(pieceOfNews.printNews())
                elif publishType == '2':
                    adText = input('Введи ТЕКСТ рекламы: ') or 'Хочу что-то продать'
                    adValidUntil = input(
                        'Введи ДАТУ, по которую будет опубликована реклама (yyyy-mm-dd): ') or (
                                               datetime.datetime.now().date() + datetime.timedelta(days=7))

                    # Parse a string into a datetime object for future calculations
                    if type(adValidUntil) == str:
                        adValidUntil = datetime.datetime.strptime(adValidUntil, "%Y-%m-%d").date()

                    if adValidUntil < datetime.datetime.now().date():
                        raise InvalidDate

                    # Instance creation of PrivateAd class
                    pieceOfPrivateAd = PrivateAd(adText, adValidUntil)
                    # A printPrivateAd function call, then the result recording to a file
                    file.write(pieceOfPrivateAd.printPrivateAd())
                elif publishType == '3':
                    horoscopeText = input('Введи ТЕКСТ гороскопа: ') or 'Все будет хорошо!'

                    # Instance creation of HoroscopeOfTheDay class
                    pieceOfHoroscope = HoroscopeOfTheDay(horoscopeText)
                    # A printHoroscopeOfTheDay function call, then the result recording to a file
                    file.write(pieceOfHoroscope.printHoroscopeOfTheDay())
                elif publishType == 'й':
                    break
                else:
                    raise InvalidPublishType
            except InvalidPublishType as error:
                print(f'\033[31m{error}\033[0m')
            except InvalidDate as error:
                print(f'\033[31m{error}\033[0m')