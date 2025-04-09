import db_connection_class
from final_task.db_connection_class import DBConnection

if __name__ == '__main__':
    city_1 = input('Укажите название ПЕРВОГО города: ')
    city_2 = input('Укажите название ВТОРОГО города: ')

    with DBConnection() as db:
        for city in [city_1, city_2]:
            if not db.ifExists(city):
                print(f"\033[31mГорода {city} нет в БД. Нужно указать координаты: \033[0m")
                latitude = float(input(f'Укажите ДОЛГОТУ для {city}: '))
                longitude = float(input(f'Укажите ШИРОТУ для {city}: '))
                db.insert(**{'city': city, 'latitude': latitude, 'longitude': longitude})

        db.calculate_distance(city_1, city_2)