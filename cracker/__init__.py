import string
import time

def crack_password(password):
    found_pw = ""
    tries = 0

    start = time.perf_counter()

    for char in password:
        time.sleep(0.2)
        if char.isdigit():
            found_pw += char
        elif char.isalpha():
            found_pw += char
        elif char in string.punctuation:
            found_pw += char

        tries += 1

    end = time.perf_counter()

    duration = (end - start) * 1000

    return {
        "password": found_pw,
        "attempts": tries,
        "duration_ms": duration,
        "cracked": True
    }