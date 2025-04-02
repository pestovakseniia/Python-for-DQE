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