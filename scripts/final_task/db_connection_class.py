import psycopg2
import db_connection_constants as dbconst
from geopy.distance import geodesic


class DBConnection:
    def __init__(self):
        self.connection = psycopg2.connect(database = dbconst.DB_NAME,
                        user = dbconst.USER,
                        host= dbconst.SERVER,
                        password = dbconst.PASSWORD,
                        port = dbconst.PORT)
        if self.connection is not None:
            print(f"\033[32mConnection to PostgreSQL.{dbconst.DB_NAME} established.\033[0m")
        self.cursor = self.connection.cursor()

        # Create table 'cities' if not yet exists
        attributes = ", ".join(f"{key} {value}" for key, value in dbconst.SCHEMA.items())
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {dbconst.TABLE} ({attributes})")

        # Populate table if it is empty
        self.cursor.execute(f"SELECT COUNT(*) FROM {dbconst.TABLE}")
        row_count = self.cursor.fetchone()[0]

        if row_count == 0:
            self.insert(**{'city': 'Батуми', 'latitude': 41.38, 'longitude': 41.37})
            self.insert(**{'city': 'Тбилиси', 'latitude': 41.72, 'longitude': 44.77})
            self.insert(**{'city': 'Нью-Йорк', 'latitude': 40.7128, 'longitude': -74.0060})
            self.insert(**{'city': 'Лондон', 'latitude': 51.5074, 'longitude': -0.1276})
            self.insert(**{'city': 'Токио', 'latitude': 35.6895, 'longitude': 139.6917})
            self.insert(**{'city': 'Сидней', 'latitude': -33.8688, 'longitude': 151.2093})
            self.insert(**{'city': 'Кейптаун', 'latitude': -33.9249, 'longitude': 18.4241})
            self.insert(**{'city': 'Москва', 'latitude': 55.7558, 'longitude': 37.6173})
            self.insert(**{'city': 'Париж', 'latitude': 48.8566, 'longitude': 2.3522})
            self.insert(**{'city': 'Рио-де-Жанейро', 'latitude': -22.9068, 'longitude': -43.1729})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        print("\033[32mConnection to PostgreSQL closed.\033[0m")

    def ifExists(self, primary_key_value, primary_key='city'):
        return bool(self.select(primary_key_value, primary_key))

    def insert(self, **kwargs):
        city = kwargs['city']
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']

        sql = f"INSERT INTO {dbconst.TABLE} (city, latitude, longitude) VALUES ('{city}', {latitude}, {longitude})"
        self.cursor.execute(sql)
        self.connection.commit()

    def select(self, primary_key_value, primary_key='city'):
        self.cursor.execute(f"SELECT latitude, longitude FROM {dbconst.TABLE} "
                            f"WHERE {primary_key} = '{primary_key_value}'")
        result = self.cursor.fetchone()
        if result:
            latitude, longitude = result
            return latitude, longitude
        else:
            return None

    def calculate_distance(self, city1, city2):
        coord1 = self.select(city1)
        coord2 = self.select(city2)

        distance_km = geodesic(coord1, coord2).kilometers
        print(f"Расстояние между {city1} и {city2}: {distance_km:.2f} км")