"""
helper functions
"""
import random
import string


def generate_random_string(length: int) -> str:
    """Generate a random string of length n"""
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
