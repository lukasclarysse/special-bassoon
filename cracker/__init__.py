import string
import time
import itertools

def crack_password(password):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    attempts = 0
    start = time.perf_counter()

    # We simulate brute force by increasing length of guesses
    for length in range(1, len(password) + 1):

        for combo in itertools.product(chars, repeat=length):
            guess = "".join(combo)
            attempts += 1

            # slow it down so you can SEE it working (optional)
            

            if guess == password:
                end = time.perf_counter()

                return {
                    "password": guess,
                    "attempts": attempts,
                    "duration_ms": round((end - start) * 1000, 2),
                    "cracked": True
                }

    end = time.perf_counter()

    return {
        "password": "",
        "attempts": attempts,
        "duration_ms": round((end - start) * 1000, 2),
        "cracked": False
    }