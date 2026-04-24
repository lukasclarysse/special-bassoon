# password-toolkit

A password generator and brute-force cracker with a lightweight web frontend. Originally built for a Python course project, now extended with multiprocessing and optimized C implementations for performance comparison.

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
    ├── cracker.py      # Python implementations (single + multi)
    └── c_impl/         # C implementations (recursive + non-recursive)
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

Open `index.html` directly in your browser.  
The page communicates with Flask at `localhost:5000`.

---

## tabs

**Generator** — configure length, character sets, and exclusions. Generates a password and copies it to your clipboard.

**Cracker** — brute-force a password using different implementations:
- Python (single-threaded) 
- Python (multiprocessing)  this one is what is used in the webapp; the other implementations are only available as source code
- C (iterative, no recursion)
- C (recursive)

**Logs** — records completed crack attempts with password, attempts, and time. Exportable as CSV or TXT.

---

## performance benchmarks

All benchmarks shown are worst-case unless stated otherwise (`~` is the last ASCII character, i.e. end of search space).

### 4-character worst case — `"~~~~"`

| implementation | time | relative speed |
|--|--|--|
| Python (single) | 18.67s | baseline |
| Python (multi) | 1.89s | ×9.88 |
| C (no recursion) | 1.21s | ×15.43 |
| C (recursion) | 1.45s | ×12.88 |

---

### 5-character worst case — `"~~~~~"`

| implementation | time | relative speed |
|--|--|--|
| Python (single) | 12.87m | baseline |
| Python (multi) | 2.88m | ×4.46 |
| C (no recursion) | 2.36m | ×5.45 |
| C (recursion) | 1.91m | ×6.76 |

---

### realistic simulation — `"r.D85"`

| implementation | time | relative speed |
|--|--|--|
| Python (multi) | 1.23m | baseline |
| C (no recursion) | 1.01m | ×1.21 |
| C (recursion) | 47.52s | ×1.55 |

---

### high complexity case — `"g7+(W}"`

| implementation | time |
|--|--|
| Python (multi) | 24.36m |
| Python (single) | 111.19m |

(≈4.5× speedup from multiprocessing)

---

## analysis

- Multiprocessing provides substantial gains for Python, especially on shorter search spaces (up to ~10× on 4-character inputs).
- C implementations significantly outperform Python due to lower-level memory and loop control.
- Non-recursive C performs best on shorter runs, but recursive C overtakes it on longer searches.
- This is likely due to improved branch prediction and cache behavior at higher iteration counts.
- Performance gains diminish as search space grows, since brute force remains exponential.

---

## notes on brute-force behavior

The cracker iterates through all 94 printable ASCII characters:
```
punctuation → digits → uppercase → lowercase
```

It tests:
- all combinations of length 1
- then length 2
- and so on…

This means:
- position in the search space matters as much as length
- late-position passwords take significantly longer

Even “early” passwords in longer lengths are expensive:
- 6-character space ≈ 689 billion combinations
- 8% of that is still ~56 billion attempts

---

## known limitations

- Pure brute-force only — no heuristics or dictionary attacks
- Performance still scales exponentially regardless of implementation
- Logs are session-only (export before refreshing)
- `pyperclip` may not work on headless Linux (frontend unaffected)

---

## takeaway

Small increases in password length drastically increase cracking time.  
Implementation improvements (multiprocessing, C) help, but do not change the exponential nature of brute force.