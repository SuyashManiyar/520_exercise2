def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def skjkasdkd(lst):
    """Find the largest prime value in the list and return the sum of its digits."""
    max_prime = 0  # start with 0 to avoid None checks
    for num in lst:
        # Only check numbers larger than current max_prime
        if num > max_prime and is_prime(num):
            max_prime = num

    # Sum digits directly (0 will return 0 automatically)
    return sum(map(int, str(max_prime)))
