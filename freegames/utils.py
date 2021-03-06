import collections
import math
import os


def floor(value, size, offset=200):
    """Floor of value given size and offset.

    >>> floor(10, 100)
    0.0
    >>> floor(120, 100)
    100.0
    >>> floor(-10, 100)
    -100.0
    >>> floor(-150, 100)
    -200.0
    >>> floor(50, 167)
    -33.0

    """
    return float(((value + offset) // size) * size - offset)


def path(filename):
    "Return full path to filename."
    filepath = os.path.realpath(__file__)
    dirpath = os.path.dirname(filepath)
    fullpath = os.path.join(dirpath, filename)
    return fullpath


class vector(collections.Sequence):
    """Two-dimensional vector.

    Vectors can be modified in place.

    """
    __slots__ = ('_x', '_y', '_hash')

    def __init__(self, x, y):
        """Initialize vector with coordinates: x, y.

        >>> v = vector(1, 2)
        >>> v.x
        1
        >>> v.y
        2

        """
        self._hash = None
        self._x = x
        self._y = y

    @property
    def x(self):
        """X-axis component of vector.

        >>> v = vector(1, 2)
        >>> v.x
        1
        >>> v.x = 3
        >>> v.x
        3

        """
        return round(self._x, 9)

    @x.setter
    def x(self, value):
        if self._hash is not None:
            raise ValueError('cannot set x after hashing')
        self._x = value

    @property
    def y(self):
        """Y-axis component of vector.

        >>> v = vector(1, 2)
        >>> v.y
        2
        >>> v.y = 5
        >>> v.y
        5

        """
        return round(self._y, 9)

    @y.setter
    def y(self, value):
        if self._hash is not None:
            raise ValueError('cannot set y after hashing')
        self._y = value

    def __hash__(self):
        """v.__hash__() -> hash(v)

        >>> v = vector(1, 2)
        >>> h = hash(v)
        >>> v.x = 2
        Traceback (most recent call last):
            ...
        ValueError: cannot set x after hashing

        """
        if self._hash is None:
            pair = (self.x, self.y)
            self._hash = hash(pair)
        return self._hash

    def __len__(self):
        """v.__len__() -> len(v)

        >>> v = vector(1, 2)
        >>> len(v)
        2

        """
        return 2

    def __getitem__(self, index):
        """v.__getitem__(v, i) -> v[i]

        >>> v = vector(3, 4)
        >>> v[0]
        3
        >>> v[1]
        4
        >>> v[2]
        Traceback (most recent call last):
            ...
        IndexError

        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def copy(self):
        """Return copy of vector.

        >>> v = vector(1, 2)
        >>> w = v.copy()
        >>> v is w
        False

        """
        type_self = type(self)
        return type_self(self._x, self._y)

    def __eq__(self, other):
        """v.__eq__(w) -> v == w

        >>> v = vector(1, 2)
        >>> w = vector(1, 2)
        >>> v == w
        True

        """
        if isinstance(other, vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        """v.__ne__(w) -> v != w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v != w
        True

        """
        if isinstance(other, vector):
            return self.x != other.x and self.y != other.y
        return NotImplemented

    def __iadd__(self, other):
        """v.__iadd__(w) -> v += w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v += w
        >>> v
        vector(4, 6)
        >>> v += 1
        >>> v
        vector(5, 7)

        """
        if self._hash is not None:
            raise ValueError('cannot add vector after hashing')
        elif isinstance(other, vector):
            self._x += other._x
            self._y += other._y
        else:
            self._x += other
            self._y += other
        return self

    def __add__(self, other):
        """v.__add__(w) -> v + w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v + w
        vector(4, 6)
        >>> v + 1
        vector(2, 3)
        >>> 2.0 + v
        vector(3.0, 4.0)

        """
        copy = self.copy()
        return copy.__iadd__(other)

    __radd__ = __add__

    def move(self, other):
        """Move vector by other (in-place).

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v.move(w)
        >>> v
        vector(4, 6)
        >>> v.move(3)
        >>> v
        vector(7, 9)

        """
        self.__iadd__(other)

    def __isub__(self, other):
        """v.__isub__(w) -> v -= w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v -= w
        >>> v
        vector(-2, -2)
        >>> v -= 1
        >>> v
        vector(-3, -3)

        """
        if self._hash is not None:
            raise ValueError('cannot subtract vector after hashing')
        elif isinstance(other, vector):
            self._x -= other._x
            self._y -= other._y
        else:
            self._x -= other
            self._y -= other
        return self

    def __sub__(self, other):
        """v.__sub__(w) -> v - w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v - w
        vector(-2, -2)
        >>> v - 1
        vector(0, 1)

        """
        copy = self.copy()
        return copy.__isub__(other)

    def __imul__(self, other):
        """v.__imul__(w) -> v *= w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v *= w
        >>> v
        vector(3, 8)
        >>> v *= 2
        >>> v
        vector(6, 16)

        """
        if self._hash is not None:
            raise ValueError('cannot multiply vector after hashing')
        elif isinstance(other, vector):
            self._x *= other._x
            self._y *= other._y
        else:
            self._x *= other
            self._y *= other
        return self

    def __mul__(self, other):
        """v.__mul__(w) -> v * w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v * w
        vector(3, 8)
        >>> v * 2
        vector(2, 4)
        >>> 3.0 * v
        vector(3.0, 6.0)

        """
        copy = self.copy()
        return copy.__imul__(other)

    __rmul__ = __mul__

    def scale(self, other):
        """Scale vector by other (in-place).

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> v.scale(w)
        >>> v
        vector(3, 8)
        >>> v.scale(0.5)
        >>> v
        vector(1.5, 4.0)

        """
        self.__imul__(other)

    def __itruediv__(self, other):
        """v.__itruediv__(w) -> v /= w

        >>> v = vector(2, 4)
        >>> w = vector(4, 8)
        >>> v /= w
        >>> v
        vector(0.5, 0.5)
        >>> v /= 2
        >>> v
        vector(0.25, 0.25)

        """
        if self._hash is not None:
            raise ValueError('cannot divide vector after hashing')
        elif isinstance(other, vector):
            self._x /= other._x
            self._y /= other._y
        else:
            self._x /= other
            self._y /= other
        return self

    def __truediv__(self, other):
        """v.__truediv__(w) -> v / w

        >>> v = vector(1, 2)
        >>> w = vector(3, 4)
        >>> w / v
        vector(3.0, 2.0)
        >>> v / 2
        vector(0.5, 1.0)

        """
        copy = self.copy()
        return copy.__itruediv__(other)

    def __neg__(self):
        """v.__neg__() -> -v

        >>> v = vector(1, 2)
        >>> -v
        vector(-1, -2)

        """
        copy = self.copy()
        copy._x = -copy._x
        copy._y = -copy._y
        return copy

    def __abs__(self):
        """v.__abs__() -> abs(v)

        >>> v = vector(3, 4)
        >>> abs(v)
        5.0

        """
        return (self._x ** 2 + self._y ** 2) ** 0.5

    def rotate(self, angle):
        """Rotate vector counter-clockwise by angle (in-place).

        >>> v = vector(1, 2)
        >>> v.rotate(90)
        >>> v == vector(-2, 1)
        True

        """
        if self._hash is not None:
            raise ValueError('cannot rotate vector after hashing')
        radians = angle * math.pi / 180.0
        cosine = math.cos(radians)
        sine = math.sin(radians)
        x = self._x
        y = self._y
        self._x = x * cosine - y * sine
        self._y = y * cosine + x * sine

    def __repr__(self):
        """v.__repr__() -> repr(v)

        >>> v = vector(1, 2)
        >>> repr(v)
        'vector(1, 2)'

        """
        type_self = type(self)
        name = type_self.__name__
        return '{}({!r}, {!r})'.format(name, self.x, self.y)
