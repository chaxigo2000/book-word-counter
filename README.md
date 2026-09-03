# Book Word Counter

A small desktop tool for word counts and word-frequency lists of eBooks and
documents. Built with Python and Tkinter — **double-click a `.py` file to
run; no terminal needed.**

## The two tools

| File | What it does |
|------|--------------|
| `count_words.py` | Counts the words in one file (EPUB / MOBI / AZW3 / TXT / DOCX / DOC / PDF). Optionally saves a **frequency table** — every word and how many times it appears — as a CSV. |
| `filter_wordfreq.py` | Reads a frequency CSV (like the one above), asks for a minimum count N, and writes the words appearing **more than N** times to `.txt` files — one word per line, most frequent first. |

## Features (`count_words.py`)

- Pick a file from a native file dialog (works on macOS and Windows)
- Optional **start phrase** — counting begins from its first occurrence
- Optional **stop phrase** — counting stops at its first occurrence (handy for
  ignoring back-matter like acknowledgements or appendices)
- Both phrases are matched case-insensitively
- After the count, you can **save a frequency CSV** (`word,frequency`, most
  frequent first). Skipping the save dialog only shows the total.

## Features (`filter_wordfreq.py`)

- File picker → frequency CSV, then a dialog asks for the minimum N
  (0 = keep every word)
- Words with a count **greater than N** are written one per line
- Output is split so **every file holds at most 5,000 words**:
  `book_gt100.txt` when they fit in one file, otherwise
  `book_gt100_part1.txt`, `book_gt100_part2.txt`, …
- Warns before overwriting existing files

## Supported formats (`count_words.py`)

| Format | Extension |
|--------|-----------|
| EPUB | `.epub` |
| Kindle MOBI | `.mobi` |
| Kindle AZW3 | `.azw3` |
| Plain text | `.txt` |
| Word (modern) | `.docx` |
| Word (legacy) | `.doc` |
| PDF | `.pdf` |

> **Note on `.doc` files:** the tool tries `antiword` first, then LibreOffice,
> and falls back to a basic binary extraction if neither is installed. For the
> best results with legacy `.doc` files install
> [antiword](https://formulae.brew.sh/formula/antiword)
> (`brew install antiword`) or [LibreOffice](https://www.libreoffice.org).

## Requirements

- **Python 3.9+** — the default [python.org](https://www.python.org/downloads/)
  installer includes **Tkinter**, which both tools need.
  On Windows, tick **"Add Python to PATH"** during installation so that a
  double-click launches the interpreter you installed.
- Third-party packages (`ebooklib`, `beautifulsoup4`, `mobi`, `python-docx`,
  `pdfplumber`) are **installed automatically on first run** when they are
  missing. To install them in advance:

```bash
pip install ebooklib beautifulsoup4 mobi python-docx pdfplumber
```

## Usage

### Double-click (Windows and macOS)

- Double-click `count_words.py` to count words / export a frequency CSV.
- Double-click `filter_wordfreq.py` to extract the words above a threshold.

If Windows asks which app should open the file, choose **Python** (the
interpreter from the Requirements step) and tick *Always use this app*.
On macOS, the first launch of a downloaded file needs
right-click → Open → Open.

### Command line

```bash
python3 count_words.py        # count words and optionally save the CSV
python3 filter_wordfreq.py    # extract words above a frequency threshold
```

## License

MIT — see [LICENSE](LICENSE).
