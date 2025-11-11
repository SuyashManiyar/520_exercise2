from typing import List

def parse_music(music_string: str) -> List[int]:
    # Define mapping from note symbols to beat durations
    note_durations = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }

    # Split the input string by spaces
    notes = music_string.split()

    # Convert notes to their durations
    beat_durations = [note_durations[note] for note in notes if note in note_durations]

    return beat_durations

# Test the function
print(parse_music('o o| .| o| o| .| .| .| .| o o'))  
# Output: [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]

# Auto-generated alias for testing
candidate = parse_music
