# The problem asks us to calculate the sum of the digits of a number N in binary representation,
# and then convert that sum back into its binary representation as a string.
# We will first convert N to binary, then sum the digits (which are 0s and 1s), and finally convert the sum to binary.
def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary.
    
    Example
        For N = 1000, the sum of digits will be 1 the output should be "1".
        For N = 150, the sum of digits will be 6 the output should be "110".
        For N = 147, the sum of digits will be 12 the output should be "1100".
    
    Variables:
        @N integer
             Constraints: 0 ≤ N ≤ 10000.
    Output:
         a string of binary number
    """
    binary_representation = bin(N)[2:]  # Convert N to binary and remove the "0b" prefix
    digit_sum = sum(int(digit) for digit in binary_representation)  # Sum the digits in the binary representation
    binary_sum = bin(digit_sum)[2:]  # Convert the sum to binary and remove the "0b" prefix
    return binary_sum

# Auto-generated aliases for test compatibility
candidate = solve
