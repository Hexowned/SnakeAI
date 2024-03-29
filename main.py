from tkinter import *
from snake import Snake
from board import Board

root = None
canvas = None
scale = None
canvas_width = 800
canvas_height = 800

tics_per_second = 1

board_width = 25
board_height = 25
food_blocks_max = 3
wall_blocks_max = 2
test_config = False
starvation_tics = -1

snake = ()
board = None


def callback():
    update()


def main():
    global root, canvas, canvas_height, canvas_width, board, snake, scale
    root = Tk()
    root.title("Snake")
    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    scale = Scale(root, from_=0, to=250, orient=HORIZONTAL, length=canvas_width, tickinterval=25,
                  label="Turns Per Second")
    scale.set(tics_per_second)
    scale.bind("<ButtonRelease-1>", on_slider_update)
    canvas.pack()
    scale.pack(side=LEFT)
    b = Button(root, text="Next Step", command=callback)
    b.pack()
    snake = Snake(board_width, board_height, starvation_tics)
    board = Board(board_width, board_height, canvas_width, canvas_height, snake, food_blocks_max, wall_blocks_max,
                  test_config)
    board.draw(canvas)
    canvas.after(int(1000 / tics_per_second), game_loop)
    mainloop()


def game_loop():
    global canvas, tics_per_second
    if tics_per_second > 0:
        update()
        canvas.after(int(1000 / tics_per_second), game_loop)
    else:
        canvas.after(int(1000), game_loop)


def update():
    global tics_per_second, board, snake, canvas
    if snake.update(board):
        snake.reset(board)
    canvas.delete("all")
    board.draw(canvas)


def on_slider_update(event):
    global scale, tics_per_second
    tics_per_second = scale.get()


if __name__ == "__main__":
    main()
