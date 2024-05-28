from .Solver import Solver
from .Solver import Beginner
from .Solver import CFOP
from .Solver import Kociemba
from .NaiveCube import NaiveCube
from .Cubie import Cube
from .Reader import UserInput
from .Printer import TtyPrinter

__author__ = "Victor Cabezas"

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

    if isinstance(cube, UserInput):
        cube = str(cube)
    cube = _check_valid_cube(cube)

    solver = method(cube)

    return solver.solution(*args, **kwargs)


def pprint(cube, color=True):
    cube = _check_valid_cube(cube)
    printer = TtyPrinter(cube, color)
    printer.pprint()
