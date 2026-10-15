from units import Unit
import world
from random import randint
import missiles_collection
class Tank(Unit):
    def __init__(self, canvas, row, col, bot=True):
        super().__init__(canvas,
                         col * world.BLOCK_SIZE,
                         row * world.BLOCK_SIZE,
                         2,
                         8,
                         bot,
                         'tank_up')

        if bot:
            self._forward_image = 'tank_up'
            self._backward_image = 'tank_down'
            self._left_image = 'tank_left'
            self._right_image = 'tank_right'
        else:
            self._default_image = 'tank_up_player'
            self._forward_image = 'tank_up_player'
            self._backward_image = 'tank_down_player'
            self._left_image = 'tank_left_player'
            self._right_image = 'tank_right_player'

        self.forward()
        self._ammo = 80
        self._usual_speed = self._speed
        self._water_speed = self._speed // 2
        self._target = None
    def set_target(self, target):
        self._target = target
    def _AI_goto_target(self):
        if randint(1, 2) == 1:
            if self._target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self._target.get_y()<self.get_y():
                self.forward()
            else:
                self.backward()
    def _AI(self):
        if randint(1, 30) == 1:
            if randint(1, 10) < 9 and self._target is not None:
                self._AI_goto_target()
            else:
                self._change_orientation()
        elif randint(1, 30) == 1:
            self._AI_fire()
        elif randint(1, 100) == 1:
            self.fire()
    def _AI_fire(self):
        if self._target is None:
            return
        center_x = self.get_x() + self.get_size() // 2
        center_y = self.get_y() + self.get_size() // 2
        target_center_x = self._target.get_x() + self._target.get_size()//2
        target_center_y = self._target.get_y() + self._target.get_size()//2
        row = world.get_row(center_y)
        col = world.get_col(center_x)
        row_target = world.get_row(target_center_y)
        col_target = world.get_col(target_center_x)
        if row == row_target:
            if col_target < col:
                self.left()
                self.fire()
            else:
                self.right()
                self.fire()
        elif col == col_target:
            if row_target < row:
                self.forward()
                self.fire()
            else:
                self.backward()
                self.fire()
    def fire(self):
        if self._ammo > 0:
            self._ammo -= 1
            missiles_collection.fire(self)
    def _take_ammo(self):
        self._ammo += 10
        if self._ammo > 100:
            self._ammo = 100
    def get_ammo(self):
        return self._ammo
    def _set_usual_speed(self):
        self._speed = self._usual_speed
    def _set_water_speed(self):
        self._speed = self._water_speed
    def _on_map_collision(self, details):
        if world.WATER in details and len(details) == 1:
            self._set_water_speed()
        elif world.MISSILE in details:
            pos = details[world.MISSILE]
            if world.take(pos['row'], pos['col'])!= world.AIR:
                self._take_ammo()
        else:
            self._undo_move()
            if self._bot:
                self._change_orientation()
    def _no_map_collision(self):
        self._set_usual_speed()
    def _on_intersects(self, other_unit):
        super()._on_intersects(other_unit)
        if self._bot:
            self._change_orientation()
    def __str__(self):
        return f'{self._x=}, {self._y}, {self._ammo=}'
