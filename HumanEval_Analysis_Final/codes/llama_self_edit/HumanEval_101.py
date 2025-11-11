# The problem requires splitting a string of words into an array, where words can be separated by either commas or spaces.
# To solve this, we can use the replace() function to replace commas with spaces, and then use the split() function to split the string into words.
# We will handle edge cases, such as leading or trailing spaces, and return the resulting array of words.

def words_string(s):
    s = s.replace(',', ' ')  # replace commas with spaces
    s = s.split()  # split the string into words
    return s  # return the resulting array of words

# Test cases
print(words_string("Hi, my name is John")) 
print(words_string("One, two, three, four, five, six"))

# Auto-generated aliases for test compatibility
candidate = words_string
