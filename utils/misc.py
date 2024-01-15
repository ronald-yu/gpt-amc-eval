# misc utility functions
import numpy as np

def remove_non_uppercase(input_string):
    """
        Removes all non-uppercase letters in a string
    """
    return ''.join(char for char in input_string if char.isupper())

def random_mode(array):
    """
        Randomly returns one of the modes in an array.
    """
    unique_elements, counts = np.unique(array, return_counts=True)
    max_count = np.max(counts)
    modes = unique_elements[counts == max_count]
    #print(modes, max_count)
    #if len(modes)>1:
    #    return "L"
    return np.random.choice(modes)

