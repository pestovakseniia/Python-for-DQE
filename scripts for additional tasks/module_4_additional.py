import math

# Definition of constants
BUILDINGS = 2
FLOORS = 10
FLATS = 4


# Custom exception class for handling invalid workflow paths
class InvalidWorkflowPath(Exception):
    def __init__(self, message="You entered an invalid workflow path"):
        self.message = message
        super().__init__(self.message)


# Custom exception class for handling invalid flat numbers
class InvalidFlatNumberError(Exception):
    # Constructor method with a default error message
    def __init__(self, message="You entered an invalid apartment number"):
        self.message = message
        super().__init__(self.message)


# Custom exception class for handling invalid building and floor numbers
class InvalidBuildingOrFloorNumberError(Exception):
    def __init__(self, message="You entered an invalid building/floor number"):
        self.message = message
        super().__init__(self.message)


# Function to calculate the building and floor for a given flat number
# OR to calculate the flat number for a given building and floor numbers
def where_is(**kwargs):
    if "user_flat" in kwargs:
        flat_in_building = math.ceil(kwargs["user_flat"] / (FLOORS * FLATS))
        flat_in_floor = math.ceil((kwargs["user_flat"] - (flat_in_building - 1) * FLOORS * FLATS) / FLATS)
        return flat_in_building, flat_in_floor
    else:
        flats_in_building_floor = [i + ((kwargs["user_building"] - 1) * FLOORS * FLATS) + (
                kwargs["user_floor"] - 1) * FLATS for i in range(1, FLATS + 1)]
        return flats_in_building_floor


# Function to check workflow path: must be inside accepted range only
def check_workflow_path(workflow_path):
    if workflow_path not in (1, 2):
        raise InvalidWorkflowPath()


# Function to check input flat number: must be inside accepted range only
def check_flat_number(flat_number):
    if not (1 <= flat_number <= BUILDINGS * FLOORS * FLATS):
        raise InvalidFlatNumberError()


# Function to check input building and floor numbers: must be inside accepted range only
def check_building_and_floor_numbers(*args):
    if not (1 <= args[0] <= BUILDINGS) or not (1 <= args[1] <= FLOORS):
        raise InvalidBuildingOrFloorNumberError()


# Main execution block
if __name__ == '__main__':
    # Validate user input; raise an error if the flat number is out of range
    # Iterate over until user inputs a correct flat number
    while True:
        # Get the user input and validate it
        try:
            requested_workflow = int(input(
                "Choose workflow: \n(1) knowing flat number, display building and floor; \n(2) knowing building and floor, display flat number \n(PRESS 1 OR 2): "))
            check_workflow_path(requested_workflow)
            if requested_workflow == 1:
                requested_flat = int(input("Input flat #: "))
                check_flat_number(requested_flat)

                building_for_requested_flat, floor_for_requested_flat = where_is(user_flat=requested_flat)
                print(f"building: {building_for_requested_flat}, floor: {floor_for_requested_flat}")
            elif requested_workflow == 2:
                requested_building = int(input("Input building #: "))
                requested_floor = int(input("Input floor #: "))
                check_building_and_floor_numbers(requested_building, requested_floor)

                flat_out_of_building_and_floor = where_is(user_building=requested_building, user_floor=requested_floor)
                print(f"flat: {flat_out_of_building_and_floor}")
        # If input workflow path is out of scope (!= 1 or 2), handle an error
        except InvalidWorkflowPath:
            print("\033[31mYou entered the workflow path number out of accepted range. Try again\033[0m")
        # If input flat number is out of scope (i.e. 1 <= flat_number <= 80), handle an error
        except InvalidFlatNumberError:
            print("\033[31mYou entered the flat number out of accepted range. Try again\033[0m")
        # If input building/floor number is out of scope, handle an error
        except InvalidBuildingOrFloorNumberError:
            print("\033[31mYou entered the building or floor number out of accepted range. Try again\033[0m")
        # If user input a non-integer value, handle an error
        except ValueError:
            print("\033[31mYou entered a non-integer value. Try again\033[0m")
        # If the flat number is valid, calculate the building and floor
        else:
            break