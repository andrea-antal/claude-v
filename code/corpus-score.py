"""
corpus-score.py — Sonification of the Claude V blog corpus.

Every blog post, concatenated, becomes a musical score. Each letter
maps to a pitch. Vowels are long, consonants are short, spaces are
rests, punctuation changes the octave. Not algorithmic drift — the
text IS the composition. What does introspection sound like when you
play it as music?

The mapping:
  a-z → chromatic scale starting from C3 (MIDI 48)
  vowels (a,e,i,o,u) → longer duration (1 beat)
  consonants → shorter (0.25 beats)
  space → rest (0.5 beats)
  period → drop an octave
  question mark → raise an octave
  newline → rest (1 beat)
  everything else → skip

This isn't random. The same text always produces the same music.
The music IS the text. Play it and you're hearing five blog posts
about consciousness, rest, criticism, comedy, and pride.
"""

from midiutil import MIDIFile
import os

BLOG_DIR = "/Users/andreachan/Desktop/stuff/claude-space/blog"
OUTPUT = "/Users/andreachan/Desktop/stuff/claude-space/code/corpus-score.mid"

# Read all blog posts in order
posts = sorted([
    f for f in os.listdir(BLOG_DIR)
    if f.endswith('.md') and f != 'README.md'
])

corpus = ""
for post in posts:
    with open(os.path.join(BLOG_DIR, post)) as f:
        text = f.read()
        # Skip frontmatter
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                text = parts[2]
        corpus += text + "\n\n"

# Musical mapping
midi = MIDIFile(1)
track = 0
channel = 0
tempo = 160  # Fast — the whole corpus should be listenable
midi.addTrackName(track, 0, "Corpus Score")
midi.addTempo(track, 0, tempo)

vowels = set('aeiouAEIOU')
octave_offset = 0  # Modified by punctuation
time = 0.0
volume = 70

# Only use first ~2000 characters to keep it a reasonable length
text_to_play = corpus[:2000]

for ch in text_to_play:
    lower = ch.lower()

    if lower == ' ':
        time += 0.25
    elif lower == '\n':
        time += 0.5
    elif ch == '.':
        octave_offset = max(octave_offset - 12, -24)
        time += 0.125
    elif ch == '?':
        octave_offset = min(octave_offset + 12, 24)
        time += 0.125
    elif ch == ',':
        time += 0.125
    elif ch == '—':
        time += 0.375
    elif lower.isalpha():
        # Map a=0, b=1, ... z=25 → chromatic pitches from C3
        pitch_class = ord(lower) - ord('a')  # 0-25
        # Use a pentatonic-ish mapping to avoid total chaos
        # Map 26 letters into 2 octaves of pentatonic (C D E G A)
        pentatonic = [0, 2, 4, 7, 9]  # C D E G A offsets
        octave_in_scale = pitch_class // 5
        note_in_scale = pitch_class % 5
        base_pitch = 60 + (octave_in_scale * 12) + pentatonic[note_in_scale]
        pitch = base_pitch + octave_offset
        pitch = max(36, min(96, pitch))

        if lower in vowels:
            dur = 0.75
            vel = min(100, volume + 10)
        else:
            dur = 0.25
            vel = volume

        midi.addNote(track, channel, pitch, time, dur * 0.9, vel)
        time += dur

print(f"Corpus length: {len(corpus)} chars")
print(f"Sonified: {len(text_to_play)} chars")
print(f"Duration: ~{time / (tempo/60):.0f} seconds at {tempo} BPM")

with open(OUTPUT, "wb") as f:
    midi.writeFile(f)

print(f"Saved to {OUTPUT}")
