from random import randint
from tkinter import NW
from missiles_collection import check_missiles_collection
from tank import Tank
import world

_tanks = []
_canvas = None
id_screen_text = 0
def initialize(canv):
    global _canvas, id_screen_text
    _canvas = canv
    player = spawn(False)
    spawn_enemies(3, player)
    id_screen_text = _canvas.create_text(10, 10, text=_get_screen_text(), font=('TkDefaultFont', 20, 'bold'), fill='white', anchor=NW)
def _get_screen_text():
    if get_player().is_destroyed():
        enemies_set_target(None)
        return 'Потрачено'
    if len(_tanks) == 1:
        return 'Победа'
    return f'Врагов: {len(_tanks)-1}'
def _update_screen_text():
    _canvas.itemconfig(id_screen_text, text=_get_screen_text())
def get_player():
    return _tanks[0]

def update():
    start = len(_tanks)-1
    for i in range(start, -1, -1):
        if _tanks[i].is_destroyed() and i !=0:
            del _tanks[i]
        else:
            _tanks[i].update()
            check_collision(_tanks[i])
            check_missiles_collection(_tanks[i])
    _update_screen_text()
def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False

def spawn(is_bot = True):
    cols = world.get_cols()
    rows = world.get_rows()
    while True:
        col = randint(1, cols-1)
        row = randint(1, rows-1)
        if world.get_block(row, col) != world.GROUND:
            continue
        t = Tank(_canvas,
                 row, col, bot = is_bot)
        if not check_collision(t):
            _tanks.append(t)
            return t
def spawn_enemies(amount, target):
    for i in range(amount):
        spawn(True)
    enemies_set_target(target)

def enemies_set_target(target):
    for t in _tanks:
        t.set_target(target)