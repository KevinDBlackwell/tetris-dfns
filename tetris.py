#!/usr/bin/env python3
"""
Tetris resolver for the Dfns code exercise.

Reads one game per line from stdin (e.g. "L2,J4,O1,L6,J8"), drops each
piece straight down, clears full rows, and prints the final height of
each game to stdout.

    python tetris.py < games.txt > output.txt
"""
import sys

WIDTH = 10

# Cell offsets (dx, dy) for each piece. dx is added to the column from the
# input, dy=0 is the bottom row of the piece.
SHAPES = {
    "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "I": [(0, 0), (0, 1), (0, 2), (0, 3)],
    "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "Z": [(1, 0), (2, 0), (0, 1), (1, 1)],
    "L": [(0, 0), (1, 0), (0, 1), (0, 2)],
    "J": [(0, 0), (1, 0), (1, 1), (1, 2)],
    "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
}

FULL_ROW = (1 << WIDTH) - 1

# The grid is a list of ints, one per row, bottom row first.
# Bit c is set if column c in that row is filled.


def column_heights(grid):
    heights = [0] * WIDTH
    for c in range(WIDTH):
        for r in range(len(grid) - 1, -1, -1):
            if grid[r] & (1 << c):
                heights[c] = r + 1
                break
    return heights


def place_piece(grid, letter, x):
    cells = SHAPES[letter]

    # lowest cell of the piece in each column it covers
    bottoms = {}
    for dx, dy in cells:
        c = x + dx
        bottoms[c] = min(dy, bottoms.get(c, dy))

    # The piece stops as soon as any of its columns touches the stack,
    # so take the highest resting position across those columns.
    heights = column_heights(grid)
    base = max(heights[c] - dy for c, dy in bottoms.items())

    for dx, dy in cells:
        r = base + dy
        while len(grid) <= r:
            grid.append(0)
        grid[r] |= 1 << (x + dx)


def clear_full_rows(grid):
    # removing a row from the list shifts everything above it down
    grid[:] = [row for row in grid if row != FULL_ROW]


def height(grid):
    for r in range(len(grid) - 1, -1, -1):
        if grid[r]:
            return r + 1
    return 0


def resolve_game(line):
    grid = []
    for token in line.split(","):
        token = token.strip()
        if not token:
            continue
        place_piece(grid, token[0], int(token[1:]))
        # clear after every piece, since it affects where later pieces land
        clear_full_rows(grid)
    return height(grid)


def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(resolve_game(line))


if __name__ == "__main__":
    main()
