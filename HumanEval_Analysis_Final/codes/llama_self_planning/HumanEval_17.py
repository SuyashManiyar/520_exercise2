from typing import List, Tuple
import re

def parse_music(music_string: str, debug: bool = False) -> List[int]:
    """
    Convert a string of musical notes into their corresponding beat durations.
    
    Notes and their beats:
        'o'  -> 4
        'o|' -> 2
        '.|' -> 1
    """
    note_durations = {'o': 4, 'o|': 2, '.|': 1}
    music_string = music_string.replace(" ", "")
    notes = re.findall(r'o\||o|\.|', music_string)

    beat_durations = []
    i = 0
    n = len(notes)

    while i < n:
        note = notes[i]
        if note in note_durations:
            duration = note_durations[note]
            beat_durations.append(duration)
            if debug:
                print(f"Note {i}: '{note}' -> {duration} beats")
        elif debug:
            print(f"Warning: Note '{note}' at position {i} is invalid, skipping.")
        i += 1

    return beat_durations
