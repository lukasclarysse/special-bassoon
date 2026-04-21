# Password Generator — Code Summary

## Imports & Constants

```python
from random import choice, shuffle
import string
import pyperclip

CHAR_SETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "numbers": string.digits,
    "special": string.punctuation
}
```

Imports the tools needed: `choice` and `shuffle` from `random` for password construction, `string` for its built-in character set constants, and `pyperclip` for clipboard access. `CHAR_SETS` is a module-level constant that maps human-readable category names to their corresponding character strings — acting as the single source of truth for all character data used throughout the program.

---

## `get_valid_length()`

```python
def get_valid_length():
    while True:
        user_input = input("Enter the desired password length: ").strip()
        if not user_input.isdigit():
            print("Please enter a valid positive number.")
            continue

        length = int(user_input)
        if length <= 0:
            print("Length must be greater than 0.")
            continue

        return length
```

Prompts the user for a password length and loops until a valid positive integer is provided. Uses `.isdigit()` to reject non-numeric input before casting to `int`, avoiding a `ValueError`. Returns the validated length.

---

## `get_yes_no(prompt)`

```python
def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please enter 'y' or 'n'.")
```

A reusable helper that enforces a strict `y`/`n` response to any prompt. Keeps confirmation logic decoupled from the functions that need it, and loops until a valid answer is given.

---

## `configure_char_types()`

```python
def configure_char_types():
    char_type_enabled = {
        "lowercase": True,
        "uppercase": True,
        "numbers": True,
        "special": True
    }

    while True:
        print(f"\nCurrent settings: {char_type_enabled}")
        feedback = input(
            "Type a category to toggle (lowercase/uppercase/numbers/special) "
            "or press Enter to continue: "
        ).strip().lower()

        if feedback in char_type_enabled:
            char_type_enabled[feedback] = not char_type_enabled[feedback]
            print(f"Updated settings: {char_type_enabled}")
        elif feedback == "":
            if get_yes_no("Are these settings ok? (y/n): ") == "y":
                break
        else:
            print("Invalid category. No changes made.")

    return char_type_enabled
```

Handles the interactive configuration of which character types are included in the password. All four types are enabled by default. The user can toggle any category on or off by name, and pressing Enter triggers a confirmation step. The loop only exits once the user confirms their settings with `y`. Returns the final `dict` of enabled/disabled categories.

---

## `get_user_input()`

```python
def get_user_input():
    length = get_valid_length()
    char_type_enabled = configure_char_types()
    return length, char_type_enabled
```

A thin coordinator that collects all user configuration by delegating to `get_valid_length()` and `configure_char_types()`. Keeps `main()` clean by bundling the two inputs into one call.

---

## `get_excluded_chars()`

```python
def get_excluded_chars():
    excluded = input(
        "Enter any characters to exclude (or press Enter for none): "
    )
    excluded_chars = set(excluded)

    if excluded_chars:
        print(f"Excluding characters: {''.join(excluded_chars)}")
    else:
        print("No characters excluded.")

    return excluded_chars
```

Asks the user for any characters that should never appear in the password. Converts the input string to a `set` for efficient membership testing during generation. Prints a confirmation of the exclusions (or none) and returns the set.

---

## `generate_password(length, char_type_enabled, excluded_chars)`

```python
def generate_password(length, char_type_enabled, excluded_chars):
    char_pools = []

    for key, enabled in char_type_enabled.items():
        if enabled:
            filtered = ''.join(set(CHAR_SETS[key]) - excluded_chars)
            if filtered:
                char_pools.append(filtered)

    if not char_pools:
        raise ValueError("No valid characters available after exclusions.")

    if length < len(char_pools):
        raise ValueError("Length too short for selected character types.")

    password_chars = [choice(pool) for pool in char_pools]

    full_pool = ''.join(char_pools)
    password_chars += [choice(full_pool) for _ in range(length - len(char_pools))]

    shuffle(password_chars)
    return "".join(password_chars)
```

The core generation logic. For each enabled character type, it subtracts excluded characters and adds the result to `char_pools`. It then guarantees at least one character from every enabled type by seeding `password_chars` with one pick per pool. The remaining characters are drawn from the combined `full_pool`. Finally, the list is shuffled to remove any predictable ordering before being joined into the final password string. Raises descriptive `ValueError`s if the configuration makes generation impossible.

---

## `main()`

```python
def main():
    try:
        length, char_type_enabled = get_user_input()
        excluded_chars = get_excluded_chars()
        password = generate_password(length, char_type_enabled, excluded_chars)

        print(f"\nGenerated password: {password}")
        try:
            pyperclip.copy(password)
            print("Password copied to clipboard.")
        except pyperclip.PyperclipException:
            print("Could not copy to clipboard.")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

The entry point. Orchestrates the full flow: collect settings, collect exclusions, generate the password, print it, and copy it to the clipboard. Wraps everything in a `try/except` to catch and display any `ValueError` raised during generation without crashing. The `if __name__ == "__main__"` guard ensures `main()` only runs when the script is executed directly, not when imported as a module.
