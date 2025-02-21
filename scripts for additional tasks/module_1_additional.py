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

# Main execution block
if __name__ == '__main__':
    # User input for flat number
    requested_flat = int(input("Input flat #: "))

    # Validate user input; raise an error if the flat number is out of range
    if requested_flat <= 0 or requested_flat > (BUILDINGS * FLOORS * FLATS):
        raise InvalidFlatNumberError()

    # If the flat number is valid, calculate the building and floor
    building_for_requested_flat, floor_for_requested_flat = where_is_flat(FLOORS, FLATS, requested_flat)
    print(f"building: {building_for_requested_flat}, floor: {floor_for_requested_flat}")