import random
from rubik_solver.NaiveCube import NaiveCube
from rubik_solver.Cubie import Cube
from rubik_solver.Printer import TtyPrinter
from rubik_solver.RigidTransform import Pitch, Yaw, Roll, rotation
from rubik_solver.main import solve
from rubik_solver.Move import Move


# Create a cube
# Start with an unshuffled cube
cube_string = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
naive_cube = NaiveCube()
naive_cube.set_cube(cube_string)
cube = Cube()
cube.from_naive_cube(naive_cube)
# Shuffle
cube.shuffle()
naive_cube = cube.to_naive_cube()
cube_string = []
[
    cube_string.extend(naive_cube.faces[face].squares)
    for face in ["U", "L", "F", "R", "B", "D"]
]
cube_string = "".join(cube_string)
# Randomly rotate the cube
random_rotation = [random.choice(["P", "Y", "R"]) for _ in range(10)]
for t in random_rotation:
    T = rotation[t]
    cube_string = T(cube_string)


def display_cube_from_string(cube_string):
    # Apparently, we need to first create a NaiveCube object to read the cube from a string,
    # then we can convert it to a Cubie.Cube object.
    naive_cube = NaiveCube()
    naive_cube.set_cube(cube_string)
    cube = Cube()
    cube.from_naive_cube(naive_cube)
    TtyPrinter(cube, True).pprint()


print("Original orientation")
display_cube_from_string(cube_string)


# Rotate the cube
# Pitch
print("Pitched orientation")
p = Pitch()
cube_pitched = p(cube_string)
cube_double_pitched = p(cube_string, 2)
# Test
print(p(cube_pitched, -1) == cube_string)
print(p(cube_double_pitched, 2) == cube_string)
# display_cube_from_string(cube_pitched)

# Pitch
print("Yawed orientation")
y = Yaw()
cube_yawed = y(cube_string)
cube_double_yawed = y(cube_string, 2)
# Test
print(y(cube_yawed, -1) == cube_string)
print(y(cube_double_yawed, 2) == cube_string)
# display_cube_from_string(cube_yawed)

# Roll
print("Rolled orientation")
r = Roll()
cube_rolled = r(cube_string)
cube_double_rolled = r(cube_string, 2)
# Test
print(r(cube_rolled, -1) == cube_string)
print(r(cube_double_rolled, 2) == cube_string)
# display_cube_from_string(cube_rolled)


# Check if given cube is valid --- Each color should appear exactly 9 times
target_color_center = ["y", "b", "r", "g", "o", "w"]
for c in target_color_center:
    assert (
        cube_string.count(c) == 9
    ), f"Invalid cube: {c} appears {cube_string.count(c)} times"


def retrieve_center_colors(cube_str):
    """Retrieve the center colors of the cube from the string representation."""
    index_center = [4, 13, 22, 31, 40, 49]
    return [cube_str[ii] for ii in index_center]


def compare_center_colors(cube_str):
    center_colors = retrieve_center_colors(cube_str)
    return [a == b for a, b in zip(center_colors, target_color_center)]


# First check
cube_transformed = cube_string
transformation = []  # This is to record the rotation to align the centers
naligns = 0  # Number of aligned centers
while True:
    # First check --- Who knows if the cube is already valid. Plus, this is the only
    # breaking point for the while True loop.
    if all(compare_center_colors(cube_transformed)):
        break
    else:
        # Iterate over the rotation
        for t in ["P", "Y", "R"]:
            T = rotation[t]
            # For each rotation, we will only try it 4 times before moving on. After
            # trying it 4 times, the cube will be back to the original position.
            for nr in range(4):
                # Check if more centers are aligned.
                if sum(compare_center_colors(cube_transformed)) > naligns:
                    naligns += 1  # Increment the number of aligned centers
                    break
                else:
                    # If nothing is improved, rotate the cube. But, we also need to
                    # append the rotation we do to the transformation list.
                    transformation.append(t)
                    # Before moving forward, there is a chance that we rotate the cube 4
                    # times, which returns the cube to the original position. In that
                    # case, there is no need to save the 4 rotations
                    if nr == 3:
                        transformation = transformation[:-4]
                    # Apply the rotation
                    cube_transformed = T(cube_transformed)

# Solve the aligned cube
solution = solve(cube_transformed, "Kociemba")
solution = [s.raw for s in solution]
# Transform solution
for t in transformation[::-1]:  # We need to apply the transformations in reverse order
    T = rotation[t]
    solution = T.inverse_transform_move_one_positive_rotation(solution)
# Convert the solution back to Move objects
solution = [Move(s) for s in solution]
