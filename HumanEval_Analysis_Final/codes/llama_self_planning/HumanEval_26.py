from typing import List
from collections import Counter

def remove_duplicates(numbers: List[int]) -> List[int]:
    """
    Return a new list containing elements from the input list that appear only once,
    preserving the original order.
    Example: remove_duplicates([1, 2, 3, 2, 4]) -> [1, 3, 4]
    """
    count = Counter(numbers)
    result = []
    i = 0
    n = len(numbers)

    while i < n:
        num = numbers[i]
        if count[num] == 1:
            result.append(num)
        elif count[num] > 1:
            pass
        i += 1

    return result

print(remove_duplicates([1, 2, 3, 2, 4]))

candidate = remove_duplicates
