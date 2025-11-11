from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """
    Separate a flat string of balanced parenthesis groups into a list of group strings.
    Spaces in the input are ignored. Each returned element is a contiguous balanced group
    (no group contains another group). Example:
    separate_paren_groups('( ) (( )) (( )( ))') -> ['()', '(())', '(()())']
    """
    paren_string = paren_string.replace(" ", "")
    result = []
    current_group = ""
    balance = 0
    i = 0
    n = len(paren_string)

    while i < n:
        char = paren_string[i]
        current_group += char
        if char == "(":
            balance += 1
        if char == ")":
            balance -= 1
        if balance == 0 and current_group:
            result.append(current_group)
            current_group = ""
        i += 1

    return result

print(separate_paren_groups('( ) (( )) (( )( ))'))

candidate = separate_paren_groups
