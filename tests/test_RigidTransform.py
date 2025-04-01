from rubik_solver.NaiveCube import NaiveCube
from rubik_solver.Cubie import Cube
from rubik_solver.Printer import TtyPrinter
from rubik_solver.RigidTransform import Pitch, Yaw, Roll


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
cube_pitched = p.relabel_faces_one_positive_rotation(cube_string)
cube_double_pitched = p.relabel_faces_two_positive_rotation(cube_string)
# Test
print(p.relabel_faces_one_negative_rotation(cube_pitched) == cube_string)
print(p.relabel_faces_two_positive_rotation(cube_double_pitched) == cube_string)
# display_cube_from_string(cube_pitched)

# Pitch
print("Yawed orientation")
y = Yaw()
cube_yawed = y.relabel_faces_one_positive_rotation(cube_string)
cube_double_yawed = y.relabel_faces_two_positive_rotation(cube_string)
# Test
print(y.relabel_faces_one_negative_rotation(cube_yawed) == cube_string)
print(y.relabel_faces_two_positive_rotation(cube_double_yawed) == cube_string)
# display_cube_from_string(cube_yawed)

# Roll
print("Rolled orientation")
r = Roll()
cube_rolled = r.relabel_faces_one_positive_rotation(cube_string)
cube_double_rolled = r.relabel_faces_two_positive_rotation(cube_string)
# Test
print(r.relabel_faces_one_negative_rotation(cube_rolled) == cube_string)
print(r.relabel_faces_two_positive_rotation(cube_double_rolled) == cube_string)
# display_cube_from_string(cube_rolled)
