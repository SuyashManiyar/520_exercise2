# To determine if a given integer is a cube of some integer number, we need to find the cube root of the integer and check if it's an integer itself.
# We can use the round() function in combination with the ** operator to achieve this, as the cube root of a number can be calculated by raising it to the power of 1/3.
# By rounding the cube root to the nearest integer and then cubing it, we can check if the result equals the original number, indicating that it's a perfect cube.

def iscube(a):
    cube_root = round(a ** (1/3))
    return cube_root ** 3 == a

print(iscube(1))   # ==> True
print(iscube(2))   # ==> False
print(iscube(-1))  # ==> True
print(iscube(64))  # ==> True
print(iscube(0))   # ==> True
print(iscube(180)) # ==> False

# Auto-generated aliases for test compatibility
candidate = iscube
