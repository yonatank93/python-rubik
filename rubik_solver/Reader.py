from .utils import infer_bottom_center, infer_bottom_edges, infer_bottom_corners

faces = ["top", "left", "front", "right", "back", "bottom"]
colors = ["y", "b", "r", "g", "o", "w"]


class UserInput:
    def __init__(self):
        self._front = None
        self._back = None
        self._top = None
        self._bottom = None
        self._left = None
        self._right = None

        self.input_prompt()

    def input_prompt(self):
        """Promp to input cube faces and set the cube."""
        cube = {}
        for face in faces[:-1]:  # Exclude the bottom
            while True:
                face_input = input(f"Input the {face} face: ")
                try:  # Checks
                    # Check shape
                    self.shape_check(face_input)
                    # Check color input
                    self.color_check(face_input)
                    # Pass all checks
                    break
                except AssertionError:
                    continue
            cube.update({face: face_input})

        # Special case for the bottom face: user doesn't need to input it and we can
        # just infer it from the other faces
        face = faces[-1]
        while True:
            face_input = input(f"Input the {face} face: ")
            if face_input == "":  # No input from user, try to infer the face.
                # Get the faces without the bottom face
                faces_no_bottom = ""
                for ff in faces[:-1]:
                    faces_no_bottom += cube[ff]
                # Infer bottom face
                bottom_center = infer_bottom_center(faces_no_bottom)
                bottom_corners = infer_bottom_corners(faces_no_bottom)
                bottom_edges = infer_bottom_edges(faces_no_bottom)
                face_input = (
                    bottom_corners[0]
                    + bottom_edges[0]
                    + bottom_corners[1]
                    + bottom_edges[1]
                    + bottom_center
                    + bottom_edges[2]
                    + bottom_corners[2]
                    + bottom_edges[3]
                    + bottom_corners[3]
                )
                break
            else:
                try:  # Checks
                    # Check shape
                    self.shape_check(face_input)
                    # Check color input
                    self.color_check(face_input)
                    # Pass all checks
                    break
                except AssertionError:
                    continue
        cube.update({face: face_input})

        # Read the dictionary
        self.reader(cube)

    @staticmethod
    def shape_check(face):
        # Check the shape
        if len(face) != 9:
            print("Fail shape check: Need to input 9 tiles for 3 by 3 cube.")
            raise AssertionError

    @staticmethod
    def color_check(face):
        # Check the input colors
        pass_color_check = all([char in colors for char in face])
        if not pass_color_check:
            print(f"Fail color check: Make sure the colors are in {colors}")
            raise AssertionError

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, face):
        self._front = face

    @property
    def back(self):
        return self._back

    @back.setter
    def back(self, face):
        self._back = face

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, face):
        self._top = face

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, face):
        self._bottom = face

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, face):
        self._left = face

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, face):
        self._right = face

    def reader(self, cube):
        """Read the cube from a dictionary."""
        self.front = cube["front"]
        self.back = cube["back"]
        self.top = cube["top"]
        self.bottom = cube["bottom"]
        self.left = cube["left"]
        self.right = cube["right"]

    def __repr__(self):
        front = self.front
        back = self.back
        top = self.top
        bottom = self.bottom
        left = self.left
        right = self.right
        return top + left + front + right + back + bottom
