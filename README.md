# password-toolkit

A small password generator and brute-force cracker with a web frontend. Built for a Python course project.

---

## project structure

```
password-toolkit/
├── app.py              # Flask server
├── requirements.txt
├── index.html          # frontend (open directly in browser)
├── snake.js            # minigame on the cracker tab
├── generator/
│   ├── __init__.py
│   └── generator.py
└── cracker/
    ├── __init__.py
    └── cracker.py
```

---

## setup

**1. make sure you have Python 3 installed**

```bash
python --version
```

**2. install dependencies**

```bash
pip install -r requirements.txt
```

**3. start the Flask server**

```bash
python app.py
```

You should see something like:
```
 * Running on http://127.0.0.1:5000
```

**4. open the frontend**

Just open `index.html` directly in your browser — no extra server needed.
The page talks to Flask at `localhost:5000` automatically.

---

## tabs

**Generator** — configure length, character types, and any characters to exclude. Generates a password and copies it to your clipboard.

**Cracker** — paste any password and brute-force it. Works through every possible combination from length 1 upward. Realistically cracks passwords up to ~5 characters depending on complexity; anything longer will take a very long time. Play snake while you wait.

**Logs** — every completed crack attempt is logged with the password found, number of attempts, and time taken. Exportable as CSV or TXT.

---

## notes on cracker performance

Speed depends on two things: length and position in the search space. The cracker iterates through all 94 printable ASCII characters in order (punctuation first, then digits, uppercase, lowercase) and tries every combination from length 1 upward — so where your password falls in that sequence matters as much as how long it is.

Real benchmark results on a typical laptop:

| password | length | attempts | time | position in space |
|---|---|---|---|---|
| `abc` | 3 | 9K | 1ms | 1% — early |
| `c0]P` | 4 | 2.97M | 0.28s | 4% — early |
| `6{vY` | 4 | 49.8M | 4.82s | 64% — late |
| `'F1p` | 4 | 57.6M | 5.56s | 74% — late |
| `;p1M` | 4 | 65.8M | 6.42s | 84% — late |
| `2f;UN` | 5 | 4.3B | 439s | 59% — mid |
| `g7+(W}` | 6 | 56.1B | ~2h | 8% — early |

position % = attempts ÷ total combinations up to and including that length.

The key insight is that length compounds exponentially. `g7+(W}` is only 8% into the 6-character search space, but 8% of ~689 billion combinations is still 56 billion attempts — nearly 2 hours. A 4-character password late in the space (`; p1M`, 84%) cracks faster than a 6-character one that's early (8%). Beyond 6 characters, pure brute force becomes effectively impractical.

---

## known limitations

- The cracker is pure Python brute force — no dictionary attacks, no optimisations. It is intentionally simple.
- `pyperclip` (clipboard copy in the generator CLI) may not work on headless Linux without a clipboard daemon. The web frontend copies independently via the browser so this only affects running `generator.py` directly.
- Logs are session-only — they reset when you close or refresh the page. Export before closing if you want to keep them.
