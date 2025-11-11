# The problem asks to find the minimum sum of any non-empty sub-array within a given array of integers.
# We can use Kadane's algorithm to solve this problem efficiently. Kadane's algorithm is typically used for finding the maximum sub-array sum,
# but we can modify it to find the minimum sub-array sum by tracking the minimum sum so far instead of the maximum sum.
# The core idea is to iterate through the array and keep track of the current minimum sum ending at each position and the overall minimum sum encountered so far.

def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    if not nums:
        return 0  # Handle empty array case

    min_so_far = nums[0]
    current_min = nums[0]

    for i in range(1, len(nums)):
        current_min = min(nums[i], current_min + nums[i])
        min_so_far = min(min_so_far, current_min)

    return min_so_far

# Auto-generated aliases for test compatibility
candidate = minSubArraySum
