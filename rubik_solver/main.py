import argparse
import time

from .Reader import UserInput
from .utils import METHODS, pprint, solve


def main(argv=None):
    arg_parser = argparse.ArgumentParser(description="rubik_solver command line tool")
    # arg_parser.add_argument(
    #     "-i", "--cube", dest="cube", required=True, help="Cube definition string"
    # )
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

    cube = str(UserInput())  # args.cube.lower()
    print("Read cube", cube)
    pprint(cube, args.color)

    start = time.time()
    print("Solution", ", ".join(map(str, solve(cube, METHODS[args.solver]))))
    print("Solved in", time.time() - start, "seconds")
