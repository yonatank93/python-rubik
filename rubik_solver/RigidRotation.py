"""The purpose of this module is to improve the interface when Kociemba solver is
requested. Currently with this solver, the cube must be in a certain orientation: the
yellow center must be on the top face and the red center must be on the front face.
However, in theory this orientation is not necessary. That is, we can do preprocessing
to align the cube in the correct orientation, then solve the cube, and finally undo the
preprocessing. This module will be responsible for such preprocessing.

The idea is to create multiple classes for rigid body rotations: pitch, yaw, and roll.
Each class will handle relabeling the faces and transforming the solution moves. For a
convention, we set the x axis to be theh horizontal axis, the y axis to be the vertical
axis. Then pitch, yaw, and roll will be rotations around the x, y, and z axes,
respectively.
"""


class RigidRotation:
    """Base class for rigid body rotations."""

    def __init__(self):
        pass

    @property
    def index_relabel_faces_one_positive_rotation(self):
        """A list of indices that maps the original faces to the rotated faces after one
        positive rotation.
        """
        raise NotImplementedError

    def relabel_faces_one_positive_rotation(self, faces_str):
        """Relabel the faces after a positive rotation."""
        return "".join(
            [faces_str[ii] for ii in self.index_relabel_faces_one_positive_rotation]
        )

    def relabel_faces_two_positive_rotation(self, faces_str):
        """Relabel the faces after two positive rotations, i.e., rotating 180 degree."""
        return self.relabel_faces_one_positive_rotation(
            self.relabel_faces_one_positive_rotation(faces_str)
        )

    def relabel_faces_one_negative_rotation(self, faces_str):
        """Relabel the faces after a negative rotation, which is equivalent to three
        positive rotations.
        """
        return self.relabel_faces_two_positive_rotation(
            self.relabel_faces_one_positive_rotation(faces_str)
        )

    @property
    def inverse_transform_move_mapping(self):
        """A dictionary that maps the moves from the rotated cube to the original cube."""
        raise NotImplementedError

    def inverse_transform_move_one_positive_rotation(self, move_list):
        """Inverse transform the move after a positive rotation."""
        return [self.inverse_transform_move_mapping[move] for move in move_list]

    def inverse_transform_move_two_positive_rotation(self, move_list):
        """Inverse transform the move after two positive rotation, i.e., 180 degree
        rotation.
        """
        return self.inverse_transform_move_one_positive_rotation(
            self.inverse_transform_move_one_positive_rotation(move_list)
        )

    def inverse_transform_move_one_negative_rotation(self, move_list):
        """Inverse transform the move after one negative rotation, which is equivalent to
        three positive rotations.
        """
        return self.inverse_transform_move_two_positive_rotation(
            self.inverse_transform_move_one_positive_rotation(move_list)
        )

    def __call__(self, faces_str, n=1):
        """Relabel the faces after a transformation."""
        if n == 1:
            # One 90 degree positive rotation
            return self.relabel_faces_one_positive_rotation(faces_str)
        elif n == 2:
            # One 180 degree positive rotations
            return self.relabel_faces_two_positive_rotation(faces_str)
        elif n == -1:
            # One 90 degree negative rotation
            return self.relabel_faces_one_negative_rotation(faces_str)


class Pitch(RigidRotation):
    """If the x axis is the horizontal axis and the y axis is the vertical axis, then
    pitch is a rotation around the x axis. One positive pitch is a 90 degree rotation
    where the front face becomes the top face, and one negative pitch is a 90 degree
    where the bottom face becomes the top face.
    """

    def __init__(self):
        super().__init__()

    @property
    def index_relabel_faces_one_positive_rotation(self):
        """A list of indices that maps the original faces to the rotated faces after one
        positive pitch rotation.
        """
        # fmt: off
        idx = [
            18, 19, 20,
            21, 22, 23,
            24, 25, 26,
            11, 14, 17,
            10, 13, 16,
            9, 12, 15,
            45, 46, 47,
            48, 49, 50,
            51, 52, 53,
            33, 30, 27,
            34, 31, 28,
            35, 32, 29,
            8, 7, 6,
            5, 4, 3,
            2, 1, 0,
            44, 43, 42,
            41, 40, 39,
            38, 37, 36,
        ]
        # fmt: on
        return idx

    @property
    def inverse_transform_move_mapping(self):
        """A dictionary that maps the moves from the rotated cube to the original cube."""
        return {
            "R": "R",
            "R2": "R2",
            "R'": "R'",
            "L": "L",
            "L2": "L2",
            "L'": "L'",
            "U": "F",
            "U2": "F2",
            "U'": "F'",
            "D": "B",
            "D2": "B2",
            "D'": "B'",
            "F": "D",
            "F2": "D2",
            "F'": "D'",
            "B": "U",
            "B2": "U2",
            "B'": "U'",
        }


class Yaw(RigidRotation):
    """If the x axis is the horizontal axis and the y axis is the vertical axis, then
    yaw is a rotation around the y axis. One positive yaw is a 90 degree rotation where
    the left face becomes the front face, and one negative yaw is a 90 degree rotation
    where the right face becomes the front face.
    """

    def __init__(self):
        super().__init__()

    @property
    def index_relabel_faces_one_positive_rotation(self):
        """A list of indices that maps the original faces to the rotated faces after one
        positive yaw rotation.
        """
        # fmt: off
        idx = [
            2, 5, 8,
            1, 4, 7,
            0, 3, 6,
            36, 37, 38,
            39, 40, 41,
            42, 43, 44,
            9, 10, 11,
            12, 13, 14,
            15, 16, 17,
            18, 19, 20,
            21, 22, 23,
            24, 25, 26,
            27, 28, 29,
            30, 31, 32,
            33, 34, 35,
            51, 48, 45,
            52, 49, 46,
            53, 50, 47,
        ]
        # fmt: on
        return idx

    @property
    def inverse_transform_move_mapping(self):
        """A dictionary that maps the moves from the rotated cube to the original cube."""
        return {
            "R": "F",
            "R2": "F2",
            "R'": "F'",
            "L": "B",
            "L2": "B2",
            "L'": "B'",
            "U": "U",
            "U2": "U2",
            "U'": "U'",
            "D": "D",
            "D2": "D2",
            "D'": "D'",
            "F": "L",
            "F2": "L2",
            "F'": "L'",
            "B": "R",
            "B2": "R2",
            "B'": "R'",
        }


class Roll(RigidRotation):
    """If the x axis is the horizontal axis and the y axis is the vertical axis, then
    roll is a rotation around the z axis. One positive roll is a 90 degree counter
    clockwise rotation where the right face becomes the top face, and one negative roll
    is a 90 degree clockwise rotation where the left face becomes the top face.
    """

    def __init__(self):
        super().__init__()

    @property
    def index_relabel_faces_one_positive_rotation(self):
        """A list of indices that maps the original faces to the rotated faces after one
        positive roll rotation.
        """
        # fmt: off
        idx = [
            29, 32, 35,
            28, 31, 34,
            27, 30, 33,
            2, 5, 8,
            1, 4, 7,
            0, 3, 6,
            20, 23, 26,
            19, 22, 25,
            18, 21, 24,
            47, 50, 53,
            46, 49, 52,
            45, 48, 51,
            42, 39, 36,
            43, 40, 37,
            44, 41, 38,
            11, 14, 17,
            10, 13, 16,
            9, 12, 15,
        ]
        # fmt: on
        return idx

    @property
    def inverse_transform_move_mapping(self):
        """A dictionary that maps the moves from the rotated cube to the original cube."""
        return {
            "R": "D",
            "R2": "D2",
            "R'": "D'",
            "L": "U",
            "L2": "U2",
            "L'": "U'",
            "U": "R",
            "U2": "R2",
            "U'": "R'",
            "D": "L",
            "D2": "L2",
            "D'": "L'",
            "F": "F",
            "F2": "F2",
            "F'": "F'",
            "B": "B",
            "B2": "B2",
            "B'": "B'",
        }


Rotation = {"P": Pitch(), "Y": Yaw(), "R": Roll()}
