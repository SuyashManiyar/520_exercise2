# The problem asks to separate a string of parenthesized groups into a list of strings,
# where each string represents a balanced parenthesized group. We need to ignore spaces.
# The approach will be to iterate through the string, keeping track of the balance of parentheses,
# and extract the groups when the balance returns to zero.

from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    paren_string = paren_string.replace(" ", "")  # Remove spaces
    result = []
    balance = 0
    start = 0
    for i, char in enumerate(paren_string):
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance == 0:
            result.append(paren_string[start:i+1])
            start = i + 1
    return result

# Auto-generated aliases for test compatibility
candidate = separate_paren_groups
