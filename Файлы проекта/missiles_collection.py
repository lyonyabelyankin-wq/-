from units import Missile

_missiles = []
_canvas = None
def initialise(canv):
    global _canvas
    _canvas = canv
def fire(owner):
    m = Missile(_canvas, owner)
    _missiles.append(m)
def update():
    start = len(_missiles)-1
    for i in range(start, -1, -1):
        if _missiles[i].is_destroyed():
            del _missiles[i]
        else:
            _missiles[i].update()
def check_missiles_collection(tank):
    for missile in _missiles:
        if missile.get_owner() == tank:
            continue
        if missile.intersects(tank):
            missile.destroy()
            tank.damage(25)
            return
