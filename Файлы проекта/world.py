from tkinter import NW
import texture
from random import randint, choice


AIR = 'a'
GROUND = 'g'
WATER = 'w'
BRICK = 'b'
COBBLESTONE = 'c'
MISSILE = 'm'
BLOCK_SIZE = 64

def set_camera_xy(x, y):
    global _camera_x, _camera_y
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > get_width() - SCREEN_WIDTH:
        x = get_width() - SCREEN_WIDTH
    if y > get_height() - SCREEN_HEIGHT:
        y = get_height() - SCREEN_HEIGHT

    update_all = False
    if abs(_camera_x - x) >= BLOCK_SIZE or abs(_camera_y - y) >= BLOCK_SIZE:
        update_all = True

    _camera_x = x
    _camera_y = y
    # _camera_x, _camera_y = x, y

    if update_all:
        update_map(True)

def move_camera(delta_x, delta_y):
    set_camera_xy(_camera_x + delta_x, _camera_y + delta_y)

def get_screen_x(world_X):
    return world_X - _camera_x

def get_screen_y(world_Y):
    return world_Y - _camera_y


def get_rows():
    return len(_map)

def get_cols():
    return len(_map[0])

def get_width():
    return get_cols() * BLOCK_SIZE

def get_height():
    return get_rows() * BLOCK_SIZE

def get_row(y):
    return y//BLOCK_SIZE

def get_col(x):
    return x//BLOCK_SIZE

_camera_x = 0
_camera_y = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# WIDTH = SCREEN_WIDTH * 6
# HEIGHT = SCREEN_HEIGHT * 4
_canvas = None
_map = []

def create_map (rows = 20, cols = 20):
    global _map
    _map = []
    for i in range(rows):
        row = []
        for j in range(cols):
            block = GROUND
            if i == 0 or j == 0 or i == rows - 1 or j == cols - 1:
                block = COBBLESTONE
            elif randint(1,100) <= 15:
                block = choice([BRICK, WATER, COBBLESTONE, MISSILE])
            cell = _Cell(_canvas, block, j * BLOCK_SIZE, i * BLOCK_SIZE)
            row.append(cell)
        _map.append(row)
def load_map(file_name):
    global _map
    _map = []

    # Способ работы с файлом с использованием конструкции with
    with open(file_name) as f:
        i = 0
        for line in f:
            blocks = line.strip()
            row = []
            for j in range(len(blocks)):
                cell = _Cell(_canvas, blocks[j], j * BLOCK_SIZE, i * BLOCK_SIZE)
                row.append(cell)
            _map.append(row)
            i += 1
    # print(_map)
def initialize(canvas):
    global _canvas
    _canvas = canvas
    create_map(20,20)
    # load_map('./map/4.tmap')
def update_map(all = False):
    first_row = get_row(_camera_y)
    last_row = get_row(_camera_y + SCREEN_HEIGHT) + 1
    first_col = get_col(_camera_x)
    last_col = get_col(_camera_x + SCREEN_WIDTH) + 1

    if all:
        first_row = 0
        last_row = get_rows() - 1
        first_col = 0
        last_col = get_cols() - 1

    for i in range(first_row, last_row + 1):
        for j in range(first_col, last_col + 1):
            update_cell(i, j)

def update_cell(row, col):
    if _inside_of_map(row, col):
        _map[row][col].update()

def get_block(row, col):
    if _inside_of_map(row, col):
        return _map[row][col].get_block()
    return AIR

def _inside_of_map(row, col):
    return not (row < 0 or col < 0 or row >= get_rows() or col >= get_cols())

def destroy(row, col):
    if row < 1 or row >= get_rows() - 1 or col < 1 or col >= get_cols() - 1:
        return False
    return _map[row][col].destroy()

def take(row, col):
    if _inside_of_map(row, col):
        return _map[row][col].take()
    return AIR

class _Cell:
    def __init__ (self, canvas, block, x, y):
        self.__canvas = canvas
        self.__block = block
        self.__screen_x = get_screen_x(x)
        self.__screen_y = get_screen_y(y)
        self.__x = x
        self.__y = y
        self.__create_element(block)

    def __del__(self):
        self.__delete_element()

    def __delete_element(self):
        try:
            self.__canvas.delete(self.__id)
        except Exception:
            pass

    def __create_element(self,block):
        if block != GROUND:
            self.__id = self.__canvas.create_image(self.__screen_x, self.__screen_y, image = texture.get(block), anchor = NW)

    def update(self):
        if self.__block == GROUND:
            return
        screen_x = get_screen_x(self.__x)
        screen_y = get_screen_y(self.__y)

        if self.__screen_x == screen_x and self.__screen_y == screen_y:
            return

        self.__canvas.moveto(self.__id, x=screen_x, y=screen_y)

        self.__screen_x = screen_x
        self.__screen_y = screen_y

    def take(self):
        block = self.get_block()
        if block == MISSILE:
            self.set_block(GROUND)
            return block
        else:
            return AIR

    def destroy(self):
        if self.get_block() == BRICK:
            self.set_block(GROUND)
            return True
        return False

    def get_block(self):
        return self.__block

    def set_block(self, block):
        if self.__block == block:
            return
        elif block == GROUND:
            self.__delete_element()
        elif self.__block == GROUND:
            self.__create_element(block)
        else:
            self.itemconfig(self.__id, image=texture.get(block))
        self.__block = block