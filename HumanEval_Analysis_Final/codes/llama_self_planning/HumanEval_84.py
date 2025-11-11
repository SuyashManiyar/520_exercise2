# The problem asks us to find the sum of digits of a given number in binary, 
# then convert this sum into binary and return it as a string.
# To solve this, we'll first convert the number to binary, calculate the sum of its digits, 
# and then convert this sum back to binary.

def solve(N):
    binary_str = format(N, 'b')
    total = 0
    i = 0
    while i < len(binary_str):
        total += int(binary_str[i])
        i += 1
    result = format(total, 'b')
    return result

print(solve(1000))  
print(solve(150))   
print(solve(147))   

candidate = solve
