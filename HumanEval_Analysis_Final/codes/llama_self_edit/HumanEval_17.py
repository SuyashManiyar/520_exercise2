from typing import List
import re

def parse_music(music_string: str) -> List[int]:
    # Dictionary to map note symbols to beat durations
    note_durations = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }

    # Split the input string into individual notes
    notes = re.findall(r'o(?=\s|$)|o\|(?!)o|\.\|(?!o)', music_string)

    # Initialize an empty list to store the beat durations
    beat_durations = []

    # Iterate over each note and append its duration to the result list
    for note in notes:
        if note == 'o' and (notes.index(note) < len(notes) - 1 and notes[notes.index(note) + 1] == '|'):
            beat_durations.append(2)
        else:
            beat_durations.append(note_durations.get(note, note_durations.get(note + '|')))

    return beat_durations

# Test the function
print(parse_music('o o| .| o| o| .| .| .| .| o o'))

# Auto-generated aliases for test compatibility
candidate = parse_music
