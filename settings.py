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

MENU_UNITS = {
    0 : {
        'name' : 'Worker',
        'cost' : 100,
        'income' : 10,
        'size' : (1, 1)
    },
    1 : {
        'name' : 'Soldier',
        'cost' : 200,
        'income' : 20,
        'size' : (1, 1)
    },
    2 : {
        'name' : 'Tank',
        'cost' : 300,
        'income' : 30,
        'size' : (2, 2)
    },

}

MENU_RESOURCES = {
    0 : {
        'name' : 'Wood',
        'cost' : 100,
        'income' : 10,
        'size' : (1, 1)
    },
    1 : {
        'name' : 'Stone',
        'cost' : 200,
        'income' : 20,
        'size' : (1, 1)
    },
    2 : {
        'name' : 'Iron',
        'cost' : 300,
        'income' : 30,
        'size' : (1, 1)
    },
    3 : {
        'name' : 'Gold',
        'cost' : 400,
        'income' : 40,
        'size' : (1, 1)
    },
    4 : {
        'name' : 'Diamond',
        'cost' : 500,
        'income' : 50,
        'size' : (1, 1)
    }
}

MENU = {
    0 : {
        'name' : 'Buildings',
        'items' : MENU_BUILDINGS
    },
    1 : {
        'name' : 'Units',
        'items' : MENU_UNITS
    },
    2 : {
        'name' : 'Resources',
        'items' : MENU_RESOURCES
    }
}







