import world

class Hitbox:
    def __init__(self, x, y, width, height, padding=0):
        self.padding = padding
        self.__x = x
        self.__y = y
        self.__black_list = [world.WATER, world.COBBLESTONE, world.BRICK, world.MISSILE]
        self.__set_width(width)
        self.__set_height(height)

        # Геттер и Сеттер - Получение и Настройка
        # self._z   защищенный атрибут

    def __get_width(self):
        return self.__width

    def __set_width(self, width):
        if width < 0:
            width = 0
        self.__width = width

    def __get_height(self):
        return self.__height

    def __set_height(self, height):
        if height < 0:
            height = 0
        self.__height = height

    def __get_x(self):
        return self.__x

    def __set_x(self, x):
        self.__x = x

    def __get_y(self):
        return self.__y

    def __set_y(self, y):
        self.__y = y
    def set_black_list(self, black_list):
        self.__black_list = black_list
    def __get_corner_points(self):
        p_top_right = {"x" : self.right, "y" : self.top}
        p_top_left  = {"x" : self.left, "y" : self.top}
        p_bottom_right = {"x" : self.right, "y" : self.bottom}
        p_bottom_left = {"x" : self.left, "y" : self.bottom}
        return [p_top_left, p_top_right, p_bottom_right, p_bottom_left]

    def check_map_collision(self, details):
        collision = False
        for point in self.__get_corner_points():
            row = world.get_row(point["y"])
            col = world.get_col(point["x"])
            block = world.get_block(row, col)
            if block in self.__black_list:
                details[block] = {
                    "row" : row,
                    "col" : col
                }
                collision = True

        return collision


    def moveto(self, x, y):
        self.__set_x(x)
        self.__set_y(y)

    def move(self, dx, dy):
        self.__set_x(dx + self.__get_x())
        self.__set_y(dy + self.__get_y())

    def intersects(self, other):
        #Другой хитбокс левее
        if self.left > other.right:
            return False
        #Другой хитбокс правее
        elif self.right < other.left:
            return False
        #Другой хитбокс выше
        elif self.top > other.bottom:
            return False
        #Другой хитбокс ниже
        elif self.bottom < other.top:
            return False
        else:
            return True

    def __get_top(self):
        return self.y + self.padding

    def __get_bottom(self):
        return self.y + self.height - self.padding

    def __get_left(self):
        return self.x + self.padding

    def __get_right(self):
        return self.x + self.width - self.padding

    x = property(__get_x, __set_x)
    y = property(__get_y, __set_y)
    width = property(__get_width, __set_width)
    height = property(__get_height, __set_height)

    left = property(__get_left)
    right = property(__get_right)
    top = property(__get_top)
    bottom = property(__get_bottom)

    def __str__(self):
        return f"{self.__x=}, {self.__y=}, {self.__width=}, {self.__height=}"