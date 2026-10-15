# pgm-image-processor

A lightweight grayscale image processing tool written in **pure Python, no imports**. It reads and writes plain-text `.pgm` (P2) images and applies a handful of pixel-level transformations, including column/row sorting, column misalignment and a 3×3 high-pass convolution filter.

## Features

| Command | What it does |
|---|---|
| `misalign` | Reverses every odd-numbered column (1st, 3rd, 5th, …) from top to bottom, creating a striped "glitch" effect. |
| `sort_columns` | Sorts each column's pixel values in ascending order from top to bottom. |
| `sort_rows_border` | Sorts each row in ascending order from left to right, but **independently within each region** separated by black (`0`) borders. Borders may be thicker than one pixel. |
| `highpass` | Applies a 3×3 sharpening (high-pass) convolution with zero padding. Results are clamped to `[0, 255]`. |

## The `.pgm` format

The program works with ASCII grayscale PGM files:

```
P2 24 7 15
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0 0 11 11 11 11 0 0 15 15 15 15 0
...
```

- **Line 1:** `<CODE> <WIDTH> <HEIGHT> <MAX_LEVEL>`. Code is always `P2`, max level is `255`.
- **Remaining data:** whitespace-separated pixel values from top-left to bottom-right. `0` is black, `255` is white.

Images are loaded into a 2D list where `img_matrix[i][j]` is the pixel at row `i`, column `j`.

## Usage

The program reads one line from standard input in the form:

```
<INPUT_FILE> <COMMAND> <OUTPUT_FILE>
```

Examples:

```bash
echo "animals.pgm misalign animals_misalign.pgm" | python Main.py
echo "animals.pgm sort_columns animals_sort_columns.pgm" | python Main.py
echo "animals.pgm sort_rows_border animals_sort_rows_border.pgm" | python Main.py
echo "animals.pgm highpass animals_highpass.pgm" | python Main.py
```

To view the results, open the output `.pgm` files with [GIMP](https://www.gimp.org/) or any online PGM viewer, or inspect the raw values in a text editor.

## How it works

### Reading and writing
- `read_imagefile(f)` parses the header, then fills a `HEIGHT × WIDTH` matrix from the flat list of values.
- `write_imagefile(f, img_matrix)` writes a `P2` header followed by one image row per line.

### `misalign`
Copies the odd-numbered columns aside, then writes them back in reverse row order, so the top of each odd column becomes its bottom. Even-numbered columns stay untouched.

### `sort_columns`
Extracts each column, sorts it in ascending order and writes it back top to bottom.

### `sort_rows_border`
Walks each row left to right, collecting non-zero pixels into a segment. When a `0` (border) or the end of the row is reached, the segment is sorted and written back in place. Consecutive zeros are skipped, so thick borders are preserved.

### `highpass` (convolution)
The image is padded with a ring of zeros, and the kernel below is slid over every pixel:

```
[-1, -1, -1]
[-1,  9, -1]
[-1, -1, -1]
```

Each output pixel is the sum of the element-wise products, clamped to `[0, 255]`. Calculations read from the padded copy, so already-computed values never affect neighbouring results.

## Project structure

```
.
├── Main.py       # All image I/O and processing functions
└── README.md
```

## Constraints

- No external libraries or imports, only built-in Python.
- Input and output are always `.pgm` (P2) files with a max level of 255.

## Background

Developed as a homework assignment (Homework 6: Image Processing) for an introductory programming course.
