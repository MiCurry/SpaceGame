import math

class Point:
    def __init__(self, x, y, around=None):
        self.x = x
        self.y = y
        self._point = (x, y)

        if around is not None:
            self._around = around
        else:
            self._around = (x, y)

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __getitem__(self, idx) -> float:
        if idx == 0: 
            return self.x
        elif idx == 1:
            return self.y
        else:
            raise KeyError('Use either 0 for x or 1 for y')

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)

        if isinstance(other, tuple) and len(other) == 2 and all(isinstance(i, (int, float)) for i in other):
            return Point(self.x + other[0], self.y + other[1])

        raise TypeError("Unsupported operand type(s) for +: 'Point' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)

        if isinstance(other, tuple) and len(other) == 2 and all(isinstance(i, (int, float)) for i in other):
            return Point(self.x - other[0], self.y - other[1])

        raise TypeError("Unsupported operand type(s) for -: 'Point' and '{}'".format(type(other).__name__))

    def rotate_point(self, around, angle_deg):
        angle_rad = math.radians(angle_deg)

        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
        nx = self.x - around[0]
        ny = self.y - around[1]

        rx = nx * cos_a - ny * sin_a
        ry = nx * sin_a + ny * cos_a

        self.x = rx + around[0]
        self.y = ry + around[1]
        self._point = (self.x, self.y)


