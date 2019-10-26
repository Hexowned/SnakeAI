from enum import Enum


class Move(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_new_direction(self, move):
        return Direction(self.value + move.value) % 4

    def get_xy_manipulation(self):
        m = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }

        return m[self]

    def get_xy_moves(self):
        m = {
            Direction.NORTH: [Direction.NORTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                              Direction.WEST.get_xy_manipulation()],
            Direction.EAST: [Direction.NORTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                             Direction.SOUTH.get_xy_manipulation()],
            Direction.SOUTH: [Direction.SOUTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                              Direction.WEST.get_xy_manipulation()],
            Direction.WEST: [Direction.NORTH.get_xy_manipulation(), Direction.WEST.get_xy_manipulation(),
                             Direction.SOUTH.get_xy_manipulation()],
        }

        return m[self]
