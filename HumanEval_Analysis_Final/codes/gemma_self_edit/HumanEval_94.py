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
    max_prime = None
    for num in lst:
        if is_prime(num):
            if max_prime is None or num > max_prime:
                max_prime = num
    if max_prime is None:
        return 0
    return sum(int(digit) for digit in str(max_prime))

# Test cases
lst = [0,3,2,1,3,5,7,4,5,5,5,2,181,32,4,32,3,2,32,324,4,3]
print(skjkasdkd(lst))  # Expected output: 10

lst = [1,0,1,8,2,4597,2,1,3,40,1,2,1,2,4,2,5,1]
print(skjkasdkd(lst))  # Expected output: 25

lst = [1,3,1,32,5107,34,83278,109,163,23,2323,32,30,1,9,3]
print(skjkasdkd(lst))  # Expected output: 13

lst = [0,724,32,71,99,32,6,0,5,91,83,0,5,6]
print(skjkasdkd(lst))  # Expected output: 11

lst = [0,81,12,3,1,21]
print(skjkasdkd(lst))  # Expected output: 3

lst = [0,8,1,2,1,7]
print(skjkasdkd(lst))  # Expected output: 7

# Auto-generated aliases for test compatibility
candidate = is_prime
