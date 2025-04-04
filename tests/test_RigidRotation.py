import unittest
import random
from rubik_solver.NaiveCube import NaiveCube
from rubik_solver.Cubie import Cube
from rubik_solver.RigidRotation import Pitch, Yaw, Roll, Rotation
from rubik_solver.main import solve


class TestCubeTransformations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a cube
        cls.cube_string = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
        naive_cube = NaiveCube()
        naive_cube.set_cube(cls.cube_string)
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
        cls.cube_string = "".join(cube_string)

        # Randomly rotate the cube
        random_rotation = [random.choice(["P", "Y", "R"]) for _ in range(10)]
        for t in random_rotation:
            T = Rotation[t]
            cls.cube_string = T(cls.cube_string)

    def test_pitch(self):
        p = Pitch()
        cube_pitched = p(self.cube_string)
        cube_double_pitched = p(self.cube_string, 2)

        # Test
        self.assertEqual(p(cube_pitched, -1), self.cube_string)
        self.assertEqual(p(cube_double_pitched, 2), self.cube_string)

    def test_yaw(self):
        y = Yaw()
        cube_yawed = y(self.cube_string)
        cube_double_yawed = y(self.cube_string, 2)

        # Test
        self.assertEqual(y(cube_yawed, -1), self.cube_string)
        self.assertEqual(y(cube_double_yawed, 2), self.cube_string)

    def test_roll(self):
        r = Roll()
        cube_rolled = r(self.cube_string)
        cube_double_rolled = r(self.cube_string, 2)

        # Test
        self.assertEqual(r(cube_rolled, -1), self.cube_string)
        self.assertEqual(r(cube_double_rolled, 2), self.cube_string)

    def test_solution(self):
        # Convert the cube problem string into Cube object
        naive_cube = NaiveCube()
        naive_cube.set_cube(self.cube_string)
        cube = Cube()
        cube.from_naive_cube(naive_cube)

        # Solve and apply solution
        solution = solve(cube, "Kociemba")
        for s in solution:
            cube.move(s)

        # Check if cube is really solved
        nc = cube.to_naive_cube()
        assert nc.is_solved()


if __name__ == "__main__":
    unittest.main()
