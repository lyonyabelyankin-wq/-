from tkinter import N
import world
from os import listdir
def next_level():
    levels = listdir('./map')
    try:
        level_number = int(input(f'Введите номер уровня от {levels[0][:1]} до {levels[len(levels)-1][:1]} '))
        level = levels[level_number]
        world.load_map(level)
    except:
        print(f'Нужно было ввести номер уровня от {levels[0][:levels[0].find(".")]} до {levels[len(levels)-1][:levels[0].find(".")]}, а вы ввели что-то не то.')
        print('Повторите операцию ещё раз')
def menu_enter():
    print(_menu_options[_menu_current_index])
    if _menu_current_index == 3:
        pass#next_level()
    elif _menu_current_index == 4:
        window.destroy()
    change()
def controller(event):
    global _menu_current_index
    if event.keycode == KEY_UP:
        _up_down(-1)
    elif event.keycode == KEY_DOWN:
        _up_down(1)
    elif event.keycode == KEY_ESC or (event.keycode == KEY_ENTER and _menu_current_index == 0):
        change()
    elif event.keycode == KEY_ENTER:
        menu_enter()

def _up_down(move_index):
    global _menu_current_index
    _menu_current_index += move_index
    if _menu_current_index < 0:
        _menu_current_index = len(_menu_options) - 1
    elif _menu_current_index > len(_menu_options_id)-1:
        _menu_current_index = 0
    _update()
def change():
    global mode
    mode = not mode
    _update()
def create(w, window_width, window_height, canv):
    global _menu_options_id, canvas, _bg, window
    window = w
    canvas = canv
    _bg = canvas.create_rectangle(0, 0, window_width, window_height, fill='white')
    size_font = 25
    offset = size_font * 2 # для отсупов между пунктами меню
    current_offset = (window_height - offset * len(_menu_options)) // 2
    for menu_option in _menu_options:
        option_id = canvas.create_text(window_width//2,
                                       current_offset,
                                       anchor=N,
                                       font=('Arial', size_font),
                                       text=menu_option)
        _menu_options_id.append(option_id)
        current_offset += offset
    _update()

def _update():
    try:
        for menu_index in range(len(_menu_options_id)):
            element_id = _menu_options_id[menu_index]
            if mode:
                canvas.itemconfig(element_id, state='normal')
                if menu_index == _menu_current_index:
                    canvas.itemconfig(_menu_options_id[menu_index], fill='blue')
                else:
                    canvas.itemconfig(_menu_options_id[menu_index], fill='black')
            else:
                canvas.itemconfig(element_id, state='hidden')
        if not mode:
            canvas.itemconfig(_bg, state='hidden')
        else:
            canvas.itemconfig(_bg, state='normal')
    except:
        pass

mode = False

_menu_options = ['Продолжить игру',
                'Заново',
                'Сохранить',
                'Загрузить',
                'Выход']
_menu_current_index = 0
_menu_options_id = []
KEY_UP = 38
KEY_DOWN = 40
KEY_ESC = 27
KEY_ENTER = 13
window = None
canvas = None
_bg = None
