import csv_output
import content
import utils
import exceptions
import db_connection as dbc

# Main part
if __name__ == '__main__':
    # Specify input file
    input_file = 'results.txt'

    # Open a file for both writing and reading
    with open(input_file, 'a+', encoding='utf-8') as file:
        file.seek(0)
        # Condition to check if a file is empty. If it is, then write a string (written only once)
        if file.read().strip() == "":
            file.write("Новостная лента: ")

        # Create a DBConnection instance
        with content.DBConnection(dbc.SERVER, dbc.PORT, dbc.DB_NAME, dbc.USER, dbc.PASSWORD) as db:
            while True:
                try:
                    inputSource = input(
                        'Как хочешь ввести информацию: 1 - консоль, 2 - json-файл, 3 - xml-файл, й/q - завершить? ')
                    if inputSource == '1':
                        publishType = input('Что хочешь опубликовать: 1 - новость, 2 - рекламу, 3 - гороскоп? ')
                        if publishType == '1':
                            newsText = input('Введи ТЕКСТ новости: ')
                            utils.checkUserInput(newsText)

                            newsCity = input('Введи ГОРОД: ')
                            utils.checkUserInput(newsCity)

                            pieceOfNews = content.News(newsText, newsCity)  # Instance creation of News class
                            file.write(pieceOfNews.formNews())

                            db.insert_single_record('News', newsText, newsCity)
                        elif publishType == '2':
                            adText = input('Введи ТЕКСТ рекламы: ')
                            utils.checkUserInput(adText)

                            adValidUntil = input('Введи ДАТУ, по которую будет опубликована реклама (гггг-мм-дд): ')
                            utils.checkUserInput(adValidUntil)
                            utils.checkDate(adValidUntil)

                            pieceOfPrivateAd = content.PrivateAd(adText, adValidUntil)  # Instance creation of PrivateAd class
                            file.write(pieceOfPrivateAd.formPrivateAd())

                            db.insert_single_record('PrivateAd', adText, adValidUntil)
                        elif publishType == '3':
                            horoscopeText = input('Введи ТЕКСТ гороскопа: ')
                            utils.checkUserInput(horoscopeText)

                            pieceOfHoroscope = content.Horoscope(horoscopeText) # Instance creation of Horoscope class
                            file.write(pieceOfHoroscope.formHoroscope())

                            db.insert_single_record('Horoscope', horoscopeText, pieceOfHoroscope.tags_unitied)
                        else:
                            raise exceptions.InvalidPublishType
                    elif inputSource == '2':
                        userDirectory = input('Введите ПУТЬ к файлу с данными (оставьте пустым для значения по умолчанию): ') or 'text_input.json'
                        utils.checkFilePath(userDirectory)

                        dataToExport = content.TextExporterJson(userDirectory)
                        file.write(dataToExport.formObjects())

                        db.insert_from_json(dataToExport)
                    elif inputSource == '3':
                        userDirectory = input('Введите ПУТЬ к файлу с данными (оставьте пустым для значения по умолчанию): ') or 'xml_input.xml'
                        utils.checkFilePath(userDirectory)

                        dataToExport = content.TextExporterXml(userDirectory)
                        file.write(dataToExport.formObjects())

                        db.insert_from_xml(dataToExport)
                    elif inputSource in ('й', 'q'):
                        break
                    else:
                        raise exceptions.InvalidInputSource
                except exceptions.InvalidInputSource as error:
                    print(f'\033[31m{error}\033[0m')
                except exceptions.InvalidPublishType as error:
                    print(f'\033[31m{error}\033[0m')
                except exceptions.InvalidDate as error:
                    print(f'\033[31m{error}\033[0m')
                except exceptions.EmptyInput as error:
                    print(f'\033[31m{error}\033[0m')
                except exceptions.InvalidFilePath as error:
                    print(f'\033[31m{error}\033[0m')

    # Specify csv files names
    csv_1_name = 'result_1.csv'
    csv_2_name = 'result_2.csv'

    # Call functions to generate csv files with specified names
    csv_output.generate_csv_file_1(input_file, csv_1_name)
    csv_output.generate_csv_file_2(input_file, csv_2_name)