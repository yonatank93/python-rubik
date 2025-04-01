from rubik_solver.NaiveCube import NaiveCube
from rubik_solver.Cubie import Cube
from rubik_solver.Printer import TtyPrinter
from rubik_solver.RigidTransform import Pitch, Yaw, Roll


# Create a cube
cube_string = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"


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


# Get the cube string from naive_cube
naive_cube = NaiveCube()
naive_cube.set_cube(cube_string)
cube_list = []
[
    cube_list.extend(naive_cube.faces[face].squares)
    for face in ["U", "L", "F", "R", "B", "D"]
]

# Rotate the cube
# Pitch
p = Pitch()
cube_pitched = "".join(p.relabel_faces_one_positive_rotation(cube_list))
print("Pitched orientation")
display_cube_from_string(cube_pitched)

# Pitch
y = Yaw()
cube_yawed = "".join(y.relabel_faces_one_positive_rotation(cube_list))
print("Yawed orientation")
display_cube_from_string(cube_yawed)

# Pitch
y = Roll()
cube_rolled = "".join(y.relabel_faces_one_positive_rotation(cube_list))
print("Rolled orientation")
display_cube_from_string(cube_rolled)
