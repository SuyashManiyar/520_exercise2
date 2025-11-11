# The problem asks us to find the minimum sum of any non-empty sub-array of given integers, 
# we can use Kadane's algorithm which is an efficient algorithm for finding the minimum sum of subarray within an one-dimensional array of numbers.
# We will initialize two variables, one to store the current sum of sub-array and another to store the minimum sum found so far.

def minSubArraySum(nums):
    min_sum = float('inf')  
    current_sum = 0  
    for num in nums:  
        current_sum = min(num, current_sum + num)  
        min_sum = min(min_sum, current_sum)  
    return min_sum

# Test the function
print(minSubArraySum([2, 3, 4, 1, 2, 4]))  # Output: 1
print(minSubArraySum([-1, -2, -3]))  # Output: -6

# Auto-generated aliases for test compatibility
candidate = minSubArraySum
