faces = ["top", "left", "front", "right", "back", "bottom"]


class CubeDict:
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
        for face in faces:
            cube.update({face: input(f"Input the {face} face: ")})
        self.reader(cube)

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
