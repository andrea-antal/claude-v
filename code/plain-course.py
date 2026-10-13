"""Plain course of Bristol Surprise Maximus, on twelve bells in B-flat.

After the 10,032 changes rung at York Minster on 10 October 2026
(Society of Royal Cumberland Youths, 8h 22, tenor 59-1-23 in B-flat).
This is the plain course only: 528 changes, no calls. Their peal was
exactly nineteen times as long.

Tempo matches theirs: 8h 22 for 10,032 changes is ~3.0 s per change.
Twelve strikes per row plus the handstroke gap = 25 beats per whole pull,
so 250 bpm puts one strike every 0.24 s.
"""
from midiutil import MIDIFile

PN = "-5T-14.5T-5T.36.14-7T.58.16-9T.70.18-18.9T-18-1T,1T"  # CompLib
N = 12
PLACE = {c: i for i, c in enumerate("1234567890ET")}
# Bell 1 (treble) highest; bell 12 (tenor) is B-flat. Descending major scale.
PITCH = [77, 75, 74, 72, 70, 69, 67, 65, 63, 62, 60, 58]


def tokens(s):
    out, cur = [], ""
    for c in s:
        if c in "-x":
            if cur: out.append(cur); cur = ""
            out.append("x")
        elif c == ".":
            if cur: out.append(cur); cur = ""
        else:
            cur += c
    if cur: out.append(cur)
    return out


def lead(pn):
    half, end = pn.split(",")
    h, e = tokens(half), tokens(end)
    return h + h[-2::-1] + e + e[-2::-1]


def apply(row, t):
    stay = set() if t == "x" else {PLACE[c] for c in t}
    row, i = row[:], 0
    while i < N - 1:
        if i in stay or i + 1 in stay:
            i += 1
        else:
            row[i], row[i + 1] = row[i + 1], row[i]
            i += 2
    return row


def plain_course():
    rounds = list(range(1, N + 1))
    rows, row, changes = [], rounds, lead(PN)
    while True:
        for t in changes:
            row = apply(row, t)
            rows.append(row)
        if row == rounds:
            return rows


rows = plain_course()
assert len(lead(PN)) == 48
assert len(rows) == 528 and rows[-1] == list(range(1, N + 1))
assert len({tuple(r) for r in rows}) == 528  # true: no row repeats

rounds = list(range(1, N + 1))
score = [rounds] * 6 + rows + [rounds] * 4  # rounds, "go", the course, "stand"

mid = MIDIFile(1)
mid.addTempo(0, 0, 250)
mid.addProgramChange(0, 0, 0, 14)  # tubular bells
beat = 0
for i, row in enumerate(score):
    if i % 2 == 0 and i:
        beat += 1  # handstroke gap
    for bell in row:
        mid.addNote(0, 0, PITCH[bell - 1], beat, 4, 92)
        beat += 1

with open("plain-course.mid", "wb") as f:
    mid.writeFile(f)
print(f"{len(score)} rows, {beat} beats, {beat * 0.24 / 60:.1f} min")
