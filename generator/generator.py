from random import choice, shuffle
import string
import pyperclip

CHAR_SETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "numbers": string.digits,
    "special": string.punctuation
}


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


def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please enter 'y' or 'n'.")


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


def get_user_input():
    length = get_valid_length()
    char_type_enabled = configure_char_types()
    return length, char_type_enabled


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
