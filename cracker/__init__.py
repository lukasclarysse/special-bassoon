from multiprocessing import Pool, cpu_count
import itertools
import string
import time

chars = string.ascii_letters + string.digits + string.punctuation

def try_chunk(args):
    prefix, password = args
    target_length = len(password)

    # Only generate remaining length
    remaining_length = target_length - 1

    for combo in itertools.product(chars, repeat=remaining_length):
        guess = prefix + "".join(combo)

        if guess == password:
            return guess

    return None


def crack(password):
    start = time.perf_counter()

    prefixes = chars
    pool = Pool(cpu_count())

    for result in pool.imap_unordered(try_chunk, [(p, password) for p in prefixes]):
        if result:
            pool.terminate()
            end = time.perf_counter()

            return {
                "password": result,
                "duration_ms": round((end - start) * 1000, 2),
                "cracked": True
            }

    pool.close()
    pool.join()

    end = time.perf_counter()

    return {
        "password": "",
        "duration_ms": round((end - start) * 1000, 2),
        "cracked": False
    }