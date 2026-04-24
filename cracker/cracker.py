from multiprocessing import Pool, cpu_count
import itertools
import string
import time

chars = string.ascii_letters + string.digits + string.punctuation



def try_chunk(args):
    prefix, password = args
    target_length = len(password)
    remaining_length = target_length - 1

    attempts = 0

    for combo in itertools.product(chars, repeat=remaining_length):
        guess = prefix + "".join(combo)
        attempts += 1

        if guess == password:
            return (guess, attempts)

    return (None, attempts)


def crack(password):
    start = time.perf_counter()
    total_attempts = 0

    prefixes = chars
    pool = Pool(cpu_count())

    for result, attempts in pool.imap_unordered(try_chunk, [(p, password) for p in prefixes]):
        total_attempts += attempts

        if result:
            pool.terminate()
            end = time.perf_counter()

            return {
                "password": result,
                "attempts": total_attempts,
                "duration_ms": round((end - start) * 1000, 2),
                "cracked": True
            }

    pool.close()
    pool.join()

    end = time.perf_counter()

    return {
        "password": "",
        "attempts": total_attempts,
        "duration_ms": round((end - start) * 1000, 2),
        "cracked": False
    }