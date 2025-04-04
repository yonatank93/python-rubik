import argparse
import time

from .Solver import Solver, Beginner, CFOP, Kociemba
from .NaiveCube import NaiveCube
from .Cubie import Cube
from .Reader import UserInput
from .Printer import TtyPrinter
from .Move import Move
from .RigidTransform import Rotation


__author__ = "Victor Cabezas"
__maintainer__ = "Yonatan Kurniawan"

METHODS = {
    "Beginner": Beginner.BeginnerSolver,
    "CFOP": CFOP.CFOPSolver,
    "Kociemba": Kociemba.KociembaSolver,
}


def _check_valid_cube(cube):
    """Checks if cube is one of str, NaiveCube or Cubie.Cube and returns
    an instance of Cubie.Cube"""

    if isinstance(cube, str):
        c = NaiveCube()
        c.set_cube(cube)
        cube = c

    if isinstance(cube, NaiveCube):
        c = Cube()
        c.from_naive_cube(cube)
        cube = c

    if not isinstance(cube, Cube):
        raise ValueError("Cube is not one of (str, NaiveCube or Cubie.Cube)")

    return cube


def _retrieve_center_colors(cube_str):
    """Retrieve the center colors of the cube from the string representation."""
    index_center = [4, 13, 22, 31, 40, 49]
    return [cube_str[ii] for ii in index_center]


def _compare_center_colors(cube_str):
    """Compare the center colors of the cube with the target color order."""
    target_color_center = ["y", "b", "r", "g", "o", "w"]
    center_colors = _retrieve_center_colors(cube_str)
    return [a == b for a, b in zip(center_colors, target_color_center)]


def _align_centers(cube_str):
    """Do combinations of rigid rotations so that the centers of the cube are aligned in
    the following order: {top: yellow, bottom: white, left: blue, right: green,
    front: red, back: orange}.
    """
    cube_transformed = cube_str  # Copy the input cube string
    rotation_list = []  # This is to record the rotation to align the centers
    naligns = 0  # Number of aligned centers
    while True:
        # Start checking --- Who knows if the cube is already valid. Plus, this is the
        # only breaking point for the while True loop.
        if all(_compare_center_colors(cube_transformed)):
            break
        else:
            # Iterate over the rotation
            for t in ["P", "Y", "R"]:
                T = Rotation[t]
                # For each rotation, we will only try it 4 times before moving on. After
                # trying it 4 times, the cube will be back to the original position.
                for nr in range(4):
                    # Check if more centers are aligned.
                    if sum(_compare_center_colors(cube_transformed)) > naligns:
                        naligns += 1  # Increment the number of aligned centers
                        break
                    else:
                        # If nothing is improved, rotate the cube. But, we also need to
                        # append the rotation we do to the rotation list.
                        rotation_list.append(t)
                        # Before moving forward, there is a chance that we rotate the
                        # cube 4 times, which returns the cube to the original position.
                        # In that case, there is no need to save the 4 rotations.
                        if nr == 3:
                            rotation_list = rotation_list[:-4]
                        # Apply the rotation
                        cube_transformed = T(cube_transformed)
    return cube_transformed, rotation_list


def _transform_solution(solution, rotation_list):
    # Convert the solution list into a list of str
    solution_str = [s.raw for s in solution]

    # Transform solution
    for t in rotation_list[::-1]:  # Apply the transformations in reverse order
        T = Rotation[t]
        solution_str = T.inverse_transform_move_one_positive_rotation(solution_str)
    # Convert the solution back to Move objects
    solution = [Move(s) for s in solution_str]
    return solution


def solve(cube, method=Beginner.BeginnerSolver, *args, **kwargs):
    if isinstance(method, str):
        if not method in METHODS:
            raise ValueError(
                "Invalid method name, must be one of (%s)" % ", ".join(METHODS.keys())
            )
        method = METHODS[method]

    if not issubclass(method, Solver):
        raise ValueError(
            "Method %s is not a valid Solver subclass" % method.__class__.__name__
        )

    cube = _check_valid_cube(cube)

    if isinstance(cube, UserInput):
        cube = str(cube)
    # Align the centers of the cube
    if isinstance(cube, (Cube, NaiveCube)):
        if isinstance(cube, Cube):
            cube = cube.to_naive_cube()
        cube = cube.get_cube()
    aligned_cube, rotation_list = _align_centers(cube)
    # This is redundant, but it unify the format
    aligned_cube = _check_valid_cube(aligned_cube)

    # Solve --- The solver search the solution with aligned cube
    solver = method(aligned_cube)
    aligned_solution = solver.solution(*args, **kwargs)

    # Transform the solution to get solution for the original cube
    solution = _transform_solution(aligned_solution, rotation_list)
    return solution


def pprint(cube, color=True):
    cube = _check_valid_cube(cube)
    printer = TtyPrinter(cube, color)
    printer.pprint()


def main(argv=None):
    arg_parser = argparse.ArgumentParser(description="rubik_solver command line tool")
    arg_parser.add_argument("-i", "--cube", dest="cube", help="Cube definition string")
    arg_parser.add_argument(
        "-I",
        "--interactive",
        dest="per_side_input",
        action="store_true",
        help="Interactive input of cube sides",
    )
    arg_parser.add_argument(
        "-c",
        "--color",
        dest="color",
        default=True,
        action="store_false",
        help="Disable use of colors with TtyPrinter",
    )
    arg_parser.add_argument(
        "-s",
        "--solver",
        dest="solver",
        default="Beginner",
        choices=METHODS.keys(),
        help="Solver method to use",
    )
    args = arg_parser.parse_args(argv)

    if args.cube is None:
        if args.per_side_input:
            cube = str(UserInput())
        else:
            raise SystemExit
    else:
        cube = args.cube.lower()
    print("Read cube", cube)
    pprint(cube, args.color)

    start = time.time()
    print("Solution", ", ".join(map(str, solve(cube, METHODS[args.solver]))))
    print("Solved in", time.time() - start, "seconds")
