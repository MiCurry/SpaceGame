import math

from .Point import Point

class Line:
    # TODO: Should proably have setters for the length,
    # center and angle and then have those settings calls _compute_line
    # after they have been set
    def __init__(self, center : Point,
                       length : float,
                       angle_degs : float,
                       rotate_around : Point= None,
                       **kwargs):
    
        self._lenght = length
        self._center = center
        self._angle_degs = angle_degs
        self._angle_rads = math.radians(angle_degs)
        self._start : Point = None
        self._end : Point = None

        self.perturb_end = kwargs.get('perturb_end', 0.00)
        self.perturb_start = kwargs.get('perturb_start', 0.00)

        if rotate_around is not None:
            self._rotate_around = rotate_around
        else:
            self._rotate_around = center

        self._compute_line()

    @property
    def length(self) -> float:
        return self._lenght

    @property
    def center(self) -> Point:
        return self._center

    @property
    def center_x(self) -> float:
        return self._center.x

    @property
    def center_y(self) -> float:
        return self._center.y

    @property
    def angle(self) -> float:
        return self._angle_degs

    @property
    def value(self) -> tuple[float]:
        return (self._start.x, self._start.y, self._end.x, self._end.y)

    def _compute_line(self):
        half_length = self.length / 2.0

        self._start = Point(self.center.x - half_length, self.center_y + self.perturb_start)
        self._end = Point(self.center_x + half_length, self.center_y - self.perturb_start)

        # If the rotation is non-zero rotate
        if self.angle != 0.0:
            self.rotate(self._rotate_around)

    def rotate(self, around=None, angle=None):
        if around is None:
            around = self._rotate_around

        if angle is None:
            angle = self.angle

        self._start.rotate_point(around, angle)
        self._end.rotate_point(around, angle)

