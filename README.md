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

Speed depends on where the password falls in the search space, not just its length. The cracker iterates in character-set order (punctuation → digits → uppercase → lowercase roughly), so a 5-character password made of early characters like `aaaaa` cracks faster than a 4-character one near the end of the search space. This is actually a useful thing to demonstrate — password strength isn't just about length.

Rough benchmarks on a typical laptop:

| password | time |
|---|---|
| 4 chars, mixed | ~40s |
| 5 chars, early in space | ~7s |
| 5 chars, late in space | ~75s |

---

## known limitations

- The cracker is pure Python brute force — no dictionary attacks, no optimisations. It is intentionally simple.
- `pyperclip` (clipboard copy in the generator CLI) may not work on headless Linux without a clipboard daemon. The web frontend copies independently via the browser so this only affects running `generator.py` directly.
- Logs are session-only — they reset when you close or refresh the page. Export before closing if you want to keep them.
