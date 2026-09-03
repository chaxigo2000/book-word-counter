#!/usr/bin/env python3
"""
filter_wordfreq.py — GUI: keep words above a frequency threshold, split into
multiple .txt files, 5000 words per file.

Same job as a terminal version would do, but with Tkinter dialogs matching
count_words.py — no typing at the command line. Double-click to run, or:

    python filter_wordfreq.py

Flow (all native dialogs):
    1. pick the word-frequency CSV (as produced by count_words.py)
    2. enter N — words appearing MORE than N times are kept (0 keeps all)
    3. choose an output folder
    4. result popup lists the file(s) written

Filenames: <book>_gt<N>.txt when they fit in one file, otherwise
<book>_gt<N>_part1.txt, _part2.txt, ... each with at most WORDS_PER_FILE
words, one word per line, most frequent first.
"""

import os

WORDS_PER_FILE = 5000


def load_frequencies(csv_path):
    """Return a list of (word, frequency) preserving CSV order.

    Tolerates a UTF-8 BOM and an optional header row. Rows whose second
    column is not a whole number are skipped.
    """
    entries = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        first = True
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip("\r\n")
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 2:
                continue
            word, freq_raw = parts[0], parts[1]
            if first:
                first = False
                if freq_raw.strip() == "frequency":
                    continue  # header row
            try:
                freq = int(freq_raw)
            except ValueError:
                continue
            entries.append((word, freq))
    return entries


def pick_output_paths(csv_path, out_dir, n, total_words):
    """
    Decide the final .txt paths. A single file keeps a simple name; more than
    WORDS_PER_FILE words get numbered _partN files. Returns a list of paths.
    """
    stem = os.path.splitext(os.path.basename(csv_path))[0]
    base = os.path.join(out_dir, f"{stem}_gt{n}")

    if total_words <= WORDS_PER_FILE:
        return [base + ".txt"]
    parts = (total_words + WORDS_PER_FILE - 1) // WORDS_PER_FILE
    return [f"{base}_part{i}.txt" for i in range(1, parts + 1)]


def write_output_files(paths, kept_words):
    """Write the words into the given paths, chunking at WORDS_PER_FILE."""
    for i, path in enumerate(paths):
        chunk = kept_words[i * WORDS_PER_FILE:(i + 1) * WORDS_PER_FILE]
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            for word in chunk:
                f.write(word + "\n")


def run_gui():
    import sys
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog

    def log(msg):
        print(msg, flush=True)

    log(f"Book Word Counter - frequency filter (Python: {sys.executable})")
    root = tk.Tk()
    root.withdraw()

    # 1. Pick the word-frequency CSV
    log("Waiting for you to choose the word-frequency CSV file...")
    csv_path = filedialog.askopenfilename(
        title="Select a word frequency CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        parent=root,
    )
    if not csv_path:
        log("Cancelled - no CSV selected.")
        root.destroy()
        return

    entries = load_frequencies(csv_path)
    if not entries:
        log("Nothing read - is the CSV in word,frequency format?")
        messagebox.showwarning(
            "Nothing read",
            f"No rows could be read from:\n{csv_path}\n\n"
            "Is the file in word,frequency format?",
            parent=root,
        )
        root.destroy()
        return

    # 2. Ask for the minimum frequency
    log("Waiting for you to enter the minimum frequency N...")
    n = simpledialog.askinteger(
        "Minimum frequency",
        f"{len(entries):,} unique words found in:\n{csv_path}\n\n"
        "Keep words appearing MORE than N times.\n"
        "Enter N (0 = keep every word):",
        initialvalue=0,
        minvalue=0,
        parent=root,
    )
    if n is None:  # cancelled
        log("Cancelled - no N entered.")
        root.destroy()
        return

    # Keep strictly more than n, most frequent first
    kept = sorted(
        ((w, c) for w, c in entries if c > n),
        key=lambda item: (-item[1], item[0]),
    )

    if not kept:
        log(f"No words appear more than {n:,} times.")
        messagebox.showinfo(
            "No matches",
            f"No words appear more than {n:,} times in this book.\n"
            "Try a smaller N.",
            parent=root,
        )
        root.destroy()
        return

    # 3. Choose an output folder
    log("Waiting for you to choose the output folder...")
    out_dir = filedialog.askdirectory(
        title="Choose a folder for the output .txt files",
        initialdir=os.path.dirname(csv_path) or os.getcwd(),
        parent=root,
    )
    if not out_dir:  # cancelled
        log("Cancelled - no output folder chosen.")
        root.destroy()
        return

    paths = pick_output_paths(csv_path, out_dir, n, len(kept))

    # 4. Guard against silently overwriting existing files
    existing = [p for p in paths if os.path.exists(p)]
    if existing:
        answer = messagebox.askyesno(
            "Files already exist",
            "These files already exist and would be overwritten:\n\n"
            + "\n".join(existing)
            + "\n\nContinue?",
            parent=root,
        )
        if not answer:
            log("Cancelled - existing files were not overwritten.")
            root.destroy()
            return

    kept_words = [w for w, _c in kept]
    write_output_files(paths, kept_words)

    log(f"{len(kept_words):,} words kept -> {len(paths)} file(s)")
    for p in paths:
        log(f"  {p}")

    messagebox.showinfo(
        "Done",
        f"{len(kept_words):,} words appear more than {n:,} times.\n"
        f"Written as {len(paths)} file(s) at up to {WORDS_PER_FILE:,} words each:\n\n"
        + "\n".join(paths),
        parent=root,
    )
    log("Done.")
    root.destroy()


def main_entry():
    """Run the GUI; if anything fails, show the reason and keep the window open.

    Double-clicking a .py can launch a Python without Tkinter (or hit another
    startup error) — without this guard the console flashes shut in a second.
    """
    try:
        run_gui()
    except Exception as exc:  # noqa: BLE001 - we deliberately surface any error
        import sys
        import traceback

        traceback.print_exc()
        if isinstance(exc, ModuleNotFoundError) and exc.name == "tkinter":
            print("\nThis tool needs Python with Tkinter (Tcl/Tk).")
            print("Double-click 'Filter Words.bat' instead, which uses your")
            print("regular Python, or reinstall from python.org (Tkinter is")
            print("included by default).")
        else:
            print("\nThe program stopped unexpectedly - details above.")
        if sys.stdin is not None and sys.stdin.isatty():
            import os
            os.system("pause")
        sys.exit(1)


if __name__ == "__main__":
    main_entry()
