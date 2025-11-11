# The problem requires us to separate groups of nested parentheses in a given string into separate strings.
# We will use a stack-based approach to keep track of the opening and closing parentheses and form the groups.
# The main steps include removing spaces from the input string, iterating over the string to identify the groups, and appending them to the result list.

from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    paren_string = paren_string.replace(" ", "")
    result = []
    current_group = ""
    balance = 0
    for char in paren_string:
        current_group += char
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1
        if balance == 0:
            result.append(current_group)
            current_group = ""
    return result

# Test the function
print(separate_paren_groups('( ) (( )) (( )( ))'))  # Output: ('()', '(())', '(()())')

# Auto-generated aliases for test compatibility
candidate = separate_paren_groups
