# The problem requires converting integers to their roman numeral equivalents in lowercase, restricting the input range from 1 to 1000.
# To tackle this, we'll create a mapping of decimal values to their roman numeral counterparts and iterate through this mapping to construct the roman numeral string.
# We'll start from the largest decimal value and subtract it from the input number as many times as possible, appending the corresponding roman numeral to the result string each time.

def int_to_mini_roman(number):
    roman_numerals = {
        1000: 'm',
        900: 'cm',
        500: 'd',
        400: 'cd',
        100: 'c',
        90: 'xc',
        50: 'l',
        40: 'xl',
        10: 'x',
        9: 'ix',
        5: 'v',
        4: 'iv',
        1: 'i'
    }
    result = ''
    for decimal, roman in roman_numerals.items():
        while number >= decimal:
            number -= decimal
            result += roman
    return result

# Test cases
print(int_to_mini_roman(19) == 'xix')
print(int_to_mini_roman(152) == 'clii')
print(int_to_mini_roman(426) == 'cdxxvi')

# Auto-generated aliases for test compatibility
candidate = int_to_mini_roman
