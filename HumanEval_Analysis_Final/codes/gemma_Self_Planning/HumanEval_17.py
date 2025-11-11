# The problem requires parsing a string of musical notes and converting them into a list of integers representing their beat durations.
# We need to iterate through the string, identify each note type ('o', 'o|', or '.|'), and map it to its corresponding beat value (4, 2, or 1).
# The function should return a list of these beat values in the order they appear in the input string.

def parse_music(music_string: str):
    """ Input to this function is a string representing musical notes in a special ASCII format.
    Your task is to parse this string and return list of integers corresponding to how many beats does each
    not last.

    Here is a legend:
    'o' - whole note, lasts four beats
    'o|' - half note, lasts two beats
    '.|' - quater note, lasts one beat

    >>> parse_music('o o| .| o| o| .| .| .| .| o o')
    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
    """
    beats = []
    notes = music_string.split()  # Split the string into a list of individual notes
    for note in notes:
        if note == 'o':
            beats.append(4)
        elif note == 'o|':
            beats.append(2)
        elif note == '.|':
            beats.append(1)
    return beats

# Auto-generated aliases for test compatibility
candidate = parse_music
