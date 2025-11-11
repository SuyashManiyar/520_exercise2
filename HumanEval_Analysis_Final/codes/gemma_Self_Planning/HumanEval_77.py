# The problem asks to determine if a given integer is a perfect cube.
# We can achieve this by finding the cube root of the number and checking if its cube equals the original number.
# We'll handle both positive and negative numbers correctly.

def iscube(a):
    '''
    Write a function that takes an integer a and returns True 
    if this ingeger is a cube of some integer number.
    Note: you may assume the input is always valid.
    Examples:
    iscube(1) ==> True
    iscube(2) ==> False
    iscube(-1) ==> True
    iscube(64) ==> True
    iscube(0) ==> True
    iscube(180) ==> False
    '''
    if a == 0:
        return True

    # Calculate the cube root.  We use the ** operator for exponentiation.
    cube_root = round(a**(1/3))

    # Check if the cube of the cube root equals the original number.
    return cube_root**3 == a

# Auto-generated aliases for test compatibility
candidate = iscube
