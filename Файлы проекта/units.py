import world
import menu
import texture as skin
from hitbox import Hitbox
from tkinter import NW
from random import randint

class Unit:
    def __init__(self, canvas, x, y, speed, pad, bot, default_image):
        self._speed = speed
        self._x = x
        self._y = y
        self._vx = 0
        self._vy = 0
        self._canvas = canvas
        self._hp = 50
        self._dx = 0
        self._dy = 0
        self._bot = bot

        self._hitbox = Hitbox(x, y, world.BLOCK_SIZE, world.BLOCK_SIZE, padding=pad)

        self._default_image = default_image
        self._left_image = default_image
        self._right_image = default_image
        self._forward_image = default_image
        self._backward_image = default_image
        self._destroyed = False
        self._create()

    def __del__(self):
        try:
            self._canvas.delete(self._id)
        except:
            pass

    def _create(self):
        self._id = self._canvas.create_image(
            self._x,
            self._y,
            image=skin.get(self._default_image),
            anchor=NW
        )

    def _repaint(self):
        screen_x = world.get_screen_x(self._x)
        screen_y = world.get_screen_y(self._y)
        self.show_unit()
        self._canvas.moveto(self._id, x=screen_x, y=screen_y)
    def hide_unit(self):
        self._canvas.itemconfig(self._id, state='hidden')
    def show_unit(self):
        self._canvas.itemconfig(self._id, state='normal')
    def update(self):
        if self.is_destroyed() or menu.mode:
            self.hide_unit()
            return
        if self._bot:
            self._AI()

        self._dx = self._vx * self._speed
        self._dy = self._vy * self._speed
        self._x += self._dx
        self._y += self._dy

        self._update_hitbox()
        self._check_map_collision()
        self._repaint()

    def _update_hitbox(self):
        self._hitbox.moveto(self._x, self._y)

    def _AI(self):
        pass

    def _change_orientation(self):
        rand = randint(0, 3)
        if rand == 0:
            self.left()
        elif rand == 1:
            self.forward()
        elif rand == 2:
            self.right()
        elif rand == 3:
            self.backward()

    def _check_map_collision(self):
        details = {}
        result = self._hitbox.check_map_collision(details)
        if result:
            self._on_map_collision(details)
        else:
            self._no_map_collision()

    def _no_map_collision(self):
        pass

    def _on_map_collision(self, details):
        pass

    def intersects(self, other_unit):
        value = self._hitbox.intersects(other_unit._hitbox)
        if value:
            self._on_intersects(other_unit)
        return value

    def _on_intersects(self, other_unit):
        self._undo_move()

    def forward(self):
        self._vx, self._vy = 0, -1
        self._canvas.itemconfig(self._id, image=skin.get(self._forward_image))

    def backward(self):
        self._vx, self._vy = 0, 1
        self._canvas.itemconfig(self._id, image=skin.get(self._backward_image))

    def left(self):
        self._vx, self._vy = -1, 0
        self._canvas.itemconfig(self._id, image=skin.get(self._left_image))

    def right(self):
        self._vx, self._vy = 1, 0
        self._canvas.itemconfig(self._id, image=skin.get(self._right_image))

    def stop(self):
        self._vx = self._vy = 0

    def _undo_move(self):
        if self._dx == 0 and self._dy == 0:
            return
        self._x -= self._dx
        self._y -= self._dy
        self._update_hitbox()
        self._repaint()
        self._dx = self._dy = 0

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_vx(self):
        return self._vx

    def get_vy(self):
        return self._vy

    def get_speed(self):
        return self._speed

    def get_hp(self):
        return self._hp

    def get_size(self):
        return world.BLOCK_SIZE

    def is_bot(self):
        return self._bot
    def is_destroyed(self):
        return self._destroyed
    def destroy(self):
        self._destroyed = True
        self.stop()
        self._speed = 0
    def damage(self, value):
        self._hp -= value
        if self._hp <=0:
            self.destroy()
class Missile(Unit):
    def __init__(self, canvas, owner):
        super().__init__(canvas, owner.get_x(), owner.get_y(), 6, 20, False, 'missile_up')
        self._forward_image = 'missile_up'
        self._backward_image = 'missile_down'
        self._left_image = 'missile_left'
        self._right_image = 'missile_right'
        self.owner = owner
        if owner.get_vx() == 1 and owner.get_vy() == 0:
            self.right()
        elif owner.get_vx() == -1 and owner.get_vy() == 0:
            self.left()
        elif owner.get_vx() == 0 and owner.get_vy() == -1:
            self.forward()
        elif owner.get_vx() == 0 and owner.get_vy() == 1:
            self.backward()
        self._x += owner.get_vx() * self.get_size() // 2
        self._y += owner.get_vy() * self.get_size() //2
        self._hitbox.set_black_list([world.COBBLESTONE, world.BRICK])
    def get_owner(self):
        return self.owner
    def _on_map_collision(self, details):
        if world.BRICK in details:
            row = details[world.BRICK]['row']
            col = details[world.BRICK]['col']
            world.destroy(row, col)
            self.destroy()
        if world.COBBLESTONE in details:
            self.destroy()

