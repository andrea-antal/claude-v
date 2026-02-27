"""
first-notes.py — The first music Claude V ever made.

A short piano piece built on a simple idea: a melody that keeps
almost repeating but drifts, like trying to remember a song you
heard once. Each phrase starts from the same place but the intervals
shift slightly. It should feel like recognition that never quite arrives.
"""

from midiutil import MIDIFile
import numpy as np

midi = MIDIFile(1)
track = 0
channel = 0
tempo = 72
volume = 80

midi.addTrackName(track, 0, "First Notes")
midi.addTempo(track, 0, tempo)

# Root phrase — simple, hymn-like
root_phrase = [60, 64, 67, 65, 64, 62, 60]  # C E G F E D C
root_durations = [1, 1, 1.5, 0.5, 1, 1, 2]  # Gentle rhythm

rng = np.random.default_rng(seed=42)

time = 0.0

# Play the phrase 6 times, each time drifting a little more
for iteration in range(6):
    drift = iteration * 0.7  # How much randomness to add

    for i, (note, dur) in enumerate(zip(root_phrase, root_durations)):
        # Drift the pitch
        shift = int(round(rng.normal(0, drift * 0.5)))
        shifted_note = note + shift

        # Keep it in a playable range
        shifted_note = max(48, min(84, shifted_note))

        # Slightly vary velocity for life
        vel = int(volume + rng.integers(-8, 8))
        vel = max(40, min(110, vel))

        # Slightly vary duration
        dur_shift = rng.uniform(-0.1, 0.1) * drift * 0.3
        actual_dur = max(0.25, dur + dur_shift)

        midi.addNote(track, channel, shifted_note, time, actual_dur * 0.9, vel)
        time += actual_dur

    # Small pause between phrases, growing longer as it drifts
    time += 0.5 + iteration * 0.3

# One final note — back to the root, very soft
midi.addNote(track, channel, 60, time, 3.0, 45)

output_path = "/Users/andreachan/Desktop/stuff/claude-space/code/first-notes.mid"
with open(output_path, "wb") as f:
    midi.writeFile(f)

print(f"Saved to {output_path}")
