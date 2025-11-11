# I need to create a function that takes a list of integers and returns a new list with all duplicates removed, 
# keeping the original order of elements. 
# The approach will be to iterate over the input list, count the occurrences of each number, and include it in the output list only if its count is 1.

from typing import List
from collections import Counter

def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    # Count the occurrences of each number in the input list
    count = Counter(numbers)
    
    # Initialize an empty list to store the result
    result = []
    
    # Iterate over the input list
    for num in numbers:
        # If the count of the current number is 1, add it to the result list
        if count[num] == 1:
            result.append(num)
    
    # Return the result list
    return result

# Test the function
print(remove_duplicates([1, 2, 3, 2, 4]))  # Output: [1, 3, 4]

# Auto-generated aliases for test compatibility
candidate = remove_duplicates
