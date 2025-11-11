# The problem asks to remove duplicate elements from a list of integers, preserving the original order.
# We can use a dictionary (or hash map) to keep track of the frequency of each element.
# Then, we iterate through the list and only append elements to the result if their frequency is 1.

from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    counts = {}  # Dictionary to store element counts
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1

    result = []
    for number in numbers:
        if counts[number] == 1:
            result.append(number)

    return result

# Auto-generated aliases for test compatibility
candidate = remove_duplicates
