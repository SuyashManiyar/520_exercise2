# The problem asks to split a string into an array of words, where words are separated by commas or spaces.
# The approach will be to use the split() method with both comma and space as delimiters.
# We will then iterate through the resulting list and strip any leading/trailing whitespace from each word.

def words_string(s):
    """
    You will be given a string of words separated by commas or spaces. Your task is
    to split the string into words and return an array of the words.
    
    For example:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """
    words = s.replace(",", " ").split()  # Replace commas with spaces and then split by spaces
    result = []
    for word in words:
        result.append(word.strip())  # Remove leading/trailing whitespace
    return result

# Auto-generated aliases for test compatibility
candidate = words_string
