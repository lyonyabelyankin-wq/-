import world
import tanks_collection
import texture
import missiles_collection
import menu
from tkinter import *
KEY_W, KEY_A, KEY_S, KEY_D = 87, 65, 83, 68
KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT = 38, 37, 40, 39
KEY_SPACE = 32
KEY_CTRL_L = 17
FPS = 60
KEY_F = 70
def update():
    global player
    tanks_collection.update()
    missiles_collection.update()
    player = tanks_collection.get_player()
    world.set_camera_xy(
        player.get_x() - (world.SCREEN_WIDTH - player.get_size())//2,
        player.get_y() - (world.SCREEN_HEIGHT - player.get_size())//2)
    world.update_map()
    w.after(1000//FPS, update)

def game_controller(event):
    if event.keycode == KEY_W:
        player.forward()
    elif event.keycode == KEY_A:
        player.left()
    elif event.keycode == KEY_S:
        player.backward()
    elif event.keycode == KEY_D:
        player.right()
    elif event.keycode == KEY_SPACE:
        player.fire()
    if event.keycode == menu.KEY_ESC:
        menu.change()
def key_press(event):
    if menu.mode:
        menu.controller(event)
    else:
        game_controller(event)
def load_textures():
    texture.load('tank_up', './img/tank_up.png')
    texture.load('tank_down', './img/tank_down.png')
    texture.load('tank_left', './img/tank_left.png')
    texture.load('tank_right', './img/tank_right.png')

    texture.load(world.BRICK,'./img/brick.png')
    texture.load(world.WATER, './img/water.png')
    texture.load(world.COBBLESTONE, './img/wall.png')
    texture.load(world.MISSILE, "./img/bonus.png")

    texture.load('tank_down_player', './img/tank_down_player.png')
    texture.load('tank_up_player', './img/tank_up_player.png')
    texture.load('tank_left_player', './img/tank_left_player.png')
    texture.load('tank_right_player', './img/tank_right_player.png')

    texture.load('missile_up', './img/missile_up.png')
    texture.load('missile_down', './img/missile_down.png')
    texture.load('missile_left', './img/missile_left.png')
    texture.load('missile_right', './img/missile_right.png')


player = None

w = Tk()
load_textures()
w.title('Танки на минималках 2.0')
w.wm_iconphoto(False, texture.get('tank_right_player'))
canv = Canvas(w, width=world.SCREEN_WIDTH, height=world.SCREEN_HEIGHT, bg='#8ccb5e')
canv.pack()

world.initialize(canv)
tanks_collection.initialize(canv)
missiles_collection.initialise(canv)
menu.create(w, world.SCREEN_WIDTH, world.SCREEN_HEIGHT, canv)
w.bind('<KeyRelease>', key_press)#game_controller)
update()
w.mainloop()