### TASK: ###
# Create a python script:
#
# create list of 100 random numbers from 0 to 1000
# sort list from min to max (without using sort())
# calculate average for even and odd numbers
# print both average result in console
# Each line of code should be commented with description.

# import a 'random' module to facilitate work with random values
import random

# a swap helper function creation. Its purpose is to change one list's element with another
def swap(user_list, index1, index2):
    # temporary variable to store result of list[index1] value, it is needed because the next step overwrites
    # the value of list[index1] with a new value of list[index2]
    temp = user_list[index1]
    user_list[index1] = user_list[index2]
    user_list[index2] = temp

# a bubble sort algorithm implementation. It compares two neighboring elements and swaps them if the left element is
# greater than the right element.
def bubble_sort(user_list):
    # two loops are required: the inner loop compares neighboring elements, while the outer loop ensures that the
    # entire list is processed, iterating through the list multiple times until no swaps are needed
    for i1 in range(len(user_list)):
        for i2 in range(len(user_list)-1):
            if user_list[i2] > user_list[i2+1]:
                swap(user_list, i2, i2+1)

# implementation of a function that calculates average of even and odd numbers separately. The function's output is a
# dictionary
def calculate_average(user_list) -> dict:
    sum_even = 0        # variable to store the sum of all even elements is a list
    sum_odd = 0     # variable to store the sum of all odd elements is a list
    count_even = 0      # variable to store the number of all even elements in a list

    # this loop goes through each element in a list
    for number in user_list:
        # if a number is even (is divided by 2 with no remainder), then add its value to a sum_even variable and
        # increase count_even counter by 1
        if number % 2 == 0:
            sum_even += number
            count_even += 1
        # if a number is odd, add its value to a sum_odd variable
        else:
            sum_odd += number

    # calculate average for even and odd numbers separately, results will be stored in corresponding variables
    avg_even = sum_even / count_even
    avg_odd = sum_odd / (len(user_list) - count_even)        # len(list) - returns the number of elements in a list

    # the result of a function is a dictionary with keys and corresponding values
    # round function is applied to make an output more appealing
    return {'average_even': round(avg_even, 2), 'average_odd': round(avg_odd, 2)}

# using a list comprehension, I create a list of 100 random numbers from 0 to 1000 with a step 1
my_list = [random.randrange(0, 1000, 1) for i in range(100)]

# print a newly created list
print(f"initial list: {my_list}")

# call a bubble_sort function that sorts a list from min to max
bubble_sort(my_list)

# print a sorted list
print(f"sorted list: {my_list}")

# call a function that calculates average of even and odd numbers and print the result
print(calculate_average(my_list))