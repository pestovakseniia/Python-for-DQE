import math

# Definition of constants
BUILDINGS = 2
FLOORS = 10
FLATS = 4

# Custom exception class for handling invalid flat numbers
# (e.g., negative values or numbers exceeding building capacity)
class InvalidFlatNumberError(Exception):
    # Constructor method with a default error message
    def __init__(self, message = "You entered an invalid apartment number"):
        self.message = message
        super().__init__(self.message)

# Function to calculate the building and floor for a given flat number
def where_is_flat(floors, flats, user_flat):
    flat_in_building = math.ceil(user_flat / (floors * flats))
    if flat_in_building == 1:
        flat_in_floor = math.ceil(user_flat / flats)
    else:
        flat_in_floor = math.ceil((user_flat - (flat_in_building - 1) * floors * flats) / flats)
    return flat_in_building, flat_in_floor

# Function to check user input: must be inside accepted range only
def check_user_input(flat_number):
    if not (1 <= flat_number <= BUILDINGS * FLOORS * FLATS):
        raise InvalidFlatNumberError()

# Main execution block
if __name__ == '__main__':
    # Validate user input; raise an error if the flat number is out of range
    # Iterate over until user inputs a correct flat number
    while True:
        # Get the user input and validate it
        try:
            requested_flat = int(input("Input flat #: "))
            check_user_input(requested_flat)
        # If user input is out of scope (i.e. 1 <= flat_number <= 80), handle an error
        except InvalidFlatNumberError:
            print("You entered the flat number out of accepted range. Try again")
        # If user input a non-integer value, handle an error
        except ValueError:
            print("You entered the flat number out of accepted range. Try again")
        # If the flat number is valid, calculate the building and floor
        else:
            building_for_requested_flat, floor_for_requested_flat = where_is_flat(FLOORS, FLATS, requested_flat)
            print(f"building: {building_for_requested_flat}, floor: {floor_for_requested_flat}")
            break