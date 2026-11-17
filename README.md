# Tetris Resolver

Solution for the Dfns code exercise. Each line of input is a game, and the
program prints the height of what's left in the grid once all the pieces
have dropped.

## Running

Python 3, no dependencies.

```
python tetris.py < games_.txt > output.txt
```

On Mac/Linux you can also `chmod +x tetris.py` and run `./tetris.py < games_.txt`.

Input lines look like `L2,J4,O1,L6,J8`: a piece letter followed by the
column of its leftmost cell. Output is one number per line.

## Approach

- Piece shapes are stored as cell offsets from the input column, with
  `dy = 0` at the bottom of the piece. I took them from the diagram and
  checked them against the four examples in the PDF.
- Each row of the grid is a 10-bit int, bottom row first. A full row is
  `0b1111111111`.
- To drop a piece, I look at every column it covers and work out where it
  would rest on that column's stack. The piece stops at the highest of
  those, since it can't move once any part of it touches something. This is
  also why a piece can sit over a hole without falling into it (example 4).
- Full rows are cleared after every piece, not at the end, because a clear
  changes where the next piece lands. Clearing is just filtering the full
  rows out of the list, which shifts everything above down.
- The answer is the index of the top non-empty row + 1.

## Results

PDF examples:

| Input | Expected | Output |
|---|---|---|
| `O0,O2,O4,O6,O8` | 0 | 0 |
| `L0,J2,O4,L6,J8` | 2 | 2 |
| `T0,Z3,T5,J8` | 3 | 3 |
| `T0,Z3,T5,O2,O8` | 3 | 3 |

`games_.txt` gives `4, 0, 2, 2, 3, 3`.

## Tests

```
python test_tetris.py
```

Covers the PDF examples, each piece on its own, stacking, and the
stdin/stdout handling.

## Files

- `tetris.py` - the resolver
- `test_tetris.py` - tests
- `games_.txt` - sample input
- `Dfns Code Exercise.pdf` - the exercise
