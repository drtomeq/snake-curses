import _curses
import curses as cu
import time
from time import time
from random import randrange
from enum import Enum


class Directions(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4


SIDES = "#"
CORNER = "X"
SNAKE_HEAD = "+"
SNAKE_BODY = "o"
FOOD = "@"


def main(screen: _curses.window):
    def feed(pos_food, snake_head):
        return pos_food == snake_head

    def game_over(snake_pos):
        snake_head = snake_pos[-1]
        if (snake_head[0] > cu.LINES - 2 or snake_head[0] < 1 or
                snake_head[1] < 1 or snake_head[1] > cu.COLS - 2):
            screen.addstr(10, 10, "Game Over, you went over the edge")
            return True
        elif snake_head in snake_pos[:-1]:
            screen.addstr(10, 10, "Game Over, you crashed into yourself")
            return True
        else:
            return False

    def move(cords, added_dir, grow=False):
        new_cords = cords[-1].copy()
        cords.append(new_cords)
        if added_dir == Directions.RIGHT:
            cords[-1][1] += 1
        elif added_dir == Directions.LEFT:
            cords[-1][1] -= 1
        elif added_dir == Directions.DOWN:
            cords[-1][0] += 1
        elif added_dir == Directions.UP:
            cords[-1][0] -= 1
        if not grow:
            cords.pop(0)
        return cords

    def get_direct(starting):
        time_start = time()
        while time() - time_start < 0.1:
            try:
                key = screen.getkey()
            except KeyboardInterrupt:
                raise Exception("stopped by user")
            except:
                key = None
            if key == "KEY_LEFT":
                return Directions.LEFT
            elif key == "KEY_RIGHT":
                return Directions.RIGHT
            elif key == "KEY_UP":
                return Directions.UP
            elif key == "KEY_DOWN":
                return Directions.DOWN
        return starting

    def draw(food, snake):
        screen.clear()
        screen.border(SIDES, SIDES, SIDES, SIDES, CORNER, CORNER, CORNER, CORNER)
        screen.addstr(food[0], food[1], FOOD)
        screen.addstr(snake[-1][0], snake[-1][1], SNAKE_HEAD)
        for pos in snake[:-1]:
            screen.addstr(pos[0], pos[1], SNAKE_BODY)

    while True:
        food_pos = [randrange(1, cu.LINES-1), randrange(1, cu.COLS-1)]
        positions = [[randrange(1, cu.LINES-1), randrange(1, cu.COLS-1)]]
        screen.clear()
        direct = Directions.RIGHT
        screen.nodelay(True)

        while True:
            direct = get_direct(direct)
            if feed(food_pos, positions[-1]):
                positions = move(positions, direct, True)
                food_pos = [randrange(1, cu.LINES-1), randrange(1, cu.COLS-1)]
            else:
                positions = move(positions, direct)
            if game_over(positions):
                screen.refresh()
                cu.napms(2000)
                break
            draw(food_pos, positions)
            screen.refresh()


cu.wrapper(main)
