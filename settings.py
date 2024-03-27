WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
TILE_SIZE = 64


MENU_BUILDINGS = {
    0 : {
        'name' : 'House',
        'cost' : 100,
        'income' : 10,
        'size' : (2, 2)
    },
    1 : {
        'name' : 'Farm',
        'cost' : 200,
        'income' : 20,
        'size' : (2, 3)
    },
    2 : {
        'name' : 'Factory',
        'cost' : 300,
        'income' : 30,
        'size' : (3, 3)
    },
    3 : {
        'name' : 'Bank',
        'cost' : 400,
        'income' : 40,
        'size' : (3, 4)
    }
}

MENU = {
    0 : {
        'name' : 'Buildings',
        'items' : MENU_BUILDINGS
    },
    1 : {
        'name' : 'Units',
        'items' : {}
    },
    2 : {
        'name' : 'Resources',
        'items' : {}
    }
}







