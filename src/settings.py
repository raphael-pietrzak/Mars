WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

TILE_SIZE = 64

MAP_SIZE = 25

ZOOM_MAX = 70
ZOOM_MIN = 10


ASSETS = {
    0 : { 'path' : 'assets/counter.png'},
    1 : { 'path' : 'assets/settings.png'},
    2 : { 'path' : 'assets/objectives.png'},
    3 : { 'path' : 'assets/button.png'},
    4 : { 'path' : 'assets/buildings_bar.png'},   
    5 : { 'path' : 'assets/TILE_TEST.png'},
    6 : { 'path' : 'assets/build1.png'},
}

BUILDINGS = {
    0 : {'name' : 'House', 'income' : 10, 'cost' : 100, 'size' : (2, 2)},
    1 : {'name' : 'Farm', 'income' : 20, 'cost' : 200, 'size' : (2, 3)},
    2 : {'name' : 'Factory', 'income' : 30, 'cost' : 300, 'size' : (3, 3)},
    3 : {'name' : 'Bank', 'income' : 40, 'cost' : 400, 'size' : (3, 4)}
}
