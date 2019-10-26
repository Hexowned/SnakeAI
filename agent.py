import math
import random
import copy
from queue import PriorityQueue

import time

from gameobjects import GameObject
from move import Move, Direction

BOARD_SIZE = 25


class Node:
    def __init__(self, point, parent=None):
        self.point = point
        self.x = point[0]
        self.y = point[1]
        self.parent = parent
        self.h = 0
        self.g = 0
        self.f = 0

    def hasParent(self):
        return self.parent is None

    def path_to_parent(self):
        if self.parent is not None:
            # fucking gore code maar is beter dan tuple, tuple. Trust me on this one.
            return self.point + self.parent.path_to_parent()
        else:
            return self.point


def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def a_star_search(start, goal, board):
    open_list = []
    closed_list = []

    start_node = Node(start)

    open_list.append(start_node)

    while not len(open_list) == 0:
        best_node = None
        best_node_f = math.inf
        for node in open_list:
            if node.f < best_node_f:
                best_node = node
                best_node_f = node.f

        open_list.remove(best_node)

        node_north = None
        node_east = None
        node_west = None
        node_south = None

        if not (best_node.y >= BOARD_SIZE-1):
            node_south = Node((best_node.x, best_node.y+1), best_node)
        if not (best_node.y <= 0):
            node_north = Node((best_node.x, best_node.y-1), best_node)
        if not (best_node.x <= 0):
            node_west = Node((best_node.x-1, best_node.y), best_node)
        if not (best_node.x >= BOARD_SIZE-1):
            node_east = Node((best_node.x+1, best_node.y), best_node)

        successors = [node_north, node_south, node_west, node_east]

        for successor in successors:
            if successor is None:
                continue
            if successor.point == goal:
                return successor

            successor.g = 1
            successor.h = get_manhattan_distance(successor.point, goal)
            successor.f = successor.g + successor.h

            skip = False
            for node in open_list:
                if ((node.point == successor.point)):
                    skip = True
                    break

            for node in closed_list:
                if ((node.point == successor.point)):
                    skip = True
                    break

            if not skip:
                if successor.x != -1 and successor.x != BOARD_SIZE and successor.y != -1 and successor.y != BOARD_SIZE:
                    tile_object = board[successor.x][successor.y]
                    if (tile_object == GameObject.SNAKE_BODY) or (tile_object == GameObject.WALL) or (tile_object == GameObject.SNAKE_HEAD):
                        closed_list.append(successor)
                    elif (tile_object == GameObject.FOOD):
                        return successor
                    else:
                        open_list.append(successor)
                else:
                    closed_list.append(successor)

        closed_list.append(best_node)

        closed_list_num = len(closed_list)
        open_list_num = len(open_list)

    return None


class Agent:

    trial = 0
    current_score = 0
    scores = []
    path = []
    times = []

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):
        skip = False

        if (score > self.current_score):
            self.path = []
        self.current_score = score

        snek = (0, 0)
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    snek = (x, y)

        if len(self.path) == 0:

            food = []

            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == GameObject.FOOD:
                        food.append(
                            (x, y, get_manhattan_distance(snek, (x, y))))

            best_food = math.inf
            best_food_coordinate = (0, 0)
            for x in range(len(food)):
                if food[x][2] < best_food:
                    best_food = food[x][2]
                    best_food_coordinate = (food[x][0], food[x][1])

            start_time = time.time() * 1000
            a_star_node = a_star_search(snek, best_food_coordinate, board)
            end_time = time.time() * 1000
            total_time = end_time-start_time
            self.times.append(total_time)

            if a_star_node is None:
                skip = True

            else:
                raw_sauce = a_star_node.path_to_parent()

                for to_be_tuple_coordinate in range(len(raw_sauce)//2):
                    self.path.append(
                        (raw_sauce[2*to_be_tuple_coordinate], raw_sauce[2*to_be_tuple_coordinate+1]))

                self.path.pop()

        if skip:
            self.path = []

            x = random.randint(1, 3)
            if (x == 1):
                return Move.STRAIGHT
            elif (x == 2):
                return Move.RIGHT
            else:
                return Move.LEFT

        next_step = self.path.pop()

        if (direction == Direction.NORTH):
            if snek[0] != 0:
                if (snek[0]-1, snek[1]) == next_step:
                    return Move.LEFT
            if snek[1] != 0:
                if (snek[0], snek[1]-1) == next_step:
                    return Move.STRAIGHT
            if snek[0] != (BOARD_SIZE-1):
                if (snek[0]+1, snek[1]) == next_step:
                    return Move.RIGHT

        elif (direction == Direction.SOUTH):
            if snek[0] != (BOARD_SIZE-1):
                if (snek[0]+1, snek[1]) == next_step:
                    return Move.LEFT
            if snek[1] != (BOARD_SIZE-1):
                if (snek[0], snek[1] + 1) == next_step:
                    return Move.STRAIGHT
            if snek[0] != 0:
                if (snek[0]-1, snek[1]) == next_step:
                    return Move.RIGHT

        elif (direction == Direction.WEST):
            if snek[1] != (BOARD_SIZE-1):
                if (snek[0], snek[1]+1) == next_step:
                    return Move.LEFT
            if snek[0] != 0:
                if (snek[0]-1, snek[1]) == next_step:
                    return Move.STRAIGHT
            if snek[1] != 0:
                if (snek[0], snek[1] - 1) == next_step:
                    return Move.RIGHT

        elif (direction == Direction.EAST):
            if snek[1] != 0:
                if (snek[0], snek[1] - 1) == next_step:
                    return Move.LEFT
            if snek[0] != (BOARD_SIZE-1):
                if (snek[0]+1, snek[1]) == next_step:
                    return Move.STRAIGHT
            if snek[1] != (BOARD_SIZE-1):
                if (snek[0], snek[1] + 1) == next_step:
                    return Move.RIGHT

        x = random.randint(1, 3)
        if (x == 1):
            return Move.STRAIGHT
        elif (x == 2):
            return Move.RIGHT
        else:
            return Move.LEFT

    def on_die(self):
        self.scores.append(self.current_score)
        self.trial += 1

        self.path = []

        print(self.scores)
        print("average on trial ", self.trial, ":", int.average(self.scores))
        print("Average time to find path:", int.average(self.times))

        pass
