# ARNvalidator

A **hand-built deterministic finite automaton (~200 explicit states)** that validates AWS ARN strings inside documents — txt, html, csv, xlsx and docx — with a tkinter GUI for scanning files.

> Part of my lab: [rodrigo-e-g.lat](https://rodrigo-e-g.lat/es)

## What it does

Instead of a regex, the ARN grammar (`arn:aws:service:region:account:resource`) is encoded as an explicit DFA: every state (`q0`…`q199`) and every transition is written out in a transition table. The validator walks each candidate string character by character; only strings that end in an accepting state are valid ARNs.

Then it applies that automaton across real document formats:

| Format | Parser |
|---|---|
| `.txt` | plain read |
| `.html` | BeautifulSoup |
| `.csv` | csv module |
| `.xlsx` | pandas |
| `.docx` | python-docx |

Test fixtures for every format are included (`test.txt`, `test.html`, `test.csv`, `test.xlsx`, `test.docx`).

## Why a DFA instead of a regex

This started as an automata-theory exercise: prove the ARN grammar is regular by *constructing* the machine, not by borrowing `re`. Writing 200 states by hand also makes every accepted branch of the grammar visible and auditable — nothing is implicit.

## Stack

Python · tkinter · pandas · BeautifulSoup · python-docx

## Run it

```bash
pip install pandas beautifulsoup4 python-docx openpyxl
python ARNvalidator/ARNvalidator.py
# GUI: pick a file → get every ARN found, flagged valid/invalid
```

## Status

Lab project (2024). If revisited: generate the transition table from a grammar definition instead of writing states manually, and add a CLI mode for CI usage (scan a repo for malformed ARNs).
