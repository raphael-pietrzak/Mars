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




sprites_tiles = {
    1 : { 'name' : 'axe', 'path' : 'assets/tile1.png', 'type' : 'tool' },
    2 : { 'name' : 'wood blocks', 'path' : 'assets/tile2.png', 'type' : 'resource' }, 
    3 : { 'name' : 'pickaxe', 'path' : 'assets/tile3.png', 'type' : 'tool' },
    4 : { 'name' : 'decorated pickaxe', 'path' : 'assets/tile4.png', 'type' : 'tool' },
    5 : { 'name' : 'planks', 'path' : 'assets/tile5.png', 'type' : 'resource' },
    6 : { 'name' : 'fork', 'path' : 'assets/tile6.png', 'type' : 'tool' },
    7 : { 'name' : 'rock', 'path' : 'assets/tile7.png', 'type' : 'resource' },
    8 : { 'name' : 'hoe', 'path' : 'assets/tile8.png', 'type' : 'tool' },
    9 : { 'name' : 'stone', 'path' : 'assets/tile9.png', 'type' : 'resource' },
    10 : { 'name' : 'stones', 'path' : 'assets/tile10.png', 'type' : 'resource' },
    11 : { 'name' : 'shovel', 'path' : 'assets/tile11.png', 'type' : 'tool' },
    12 : { 'name' : 'straw', 'path' : 'assets/tile12.png', 'type' : 'resource' },
    13 : { 'name' : 'ciseled stone', 'path' : 'assets/tile13.png', 'type' : 'resource' },
    14 : { 'name' : 'lapiz', 'path' : 'assets/tile14.png', 'type' : 'resource' },
    15 : { 'name' : 'gold nugget', 'path' : 'assets/tile15.png', 'type' : 'resource' },
    16 : { 'name' : 'iron nugget', 'path' : 'assets/tile16.png', 'type' : 'resource' },
    17 : { 'name' : 'dirt', 'path' : 'assets/tile17.png', 'type' : 'resource' },
    18 : { 'name' : 'caillou', 'path' : 'assets/tile18.png', 'type' : 'resource' },
    19 : { 'name' : 'purple gem', 'path' : 'assets/tile19.png', 'type' : 'resource' },
    20 : { 'name' : 'orange gem', 'path' : 'assets/tile20.png', 'type' : 'resource' },
    21 : { 'name' : 'sulfur', 'path' : 'assets/tile21.png', 'type' : 'resource' },
    22 : { 'name' : 'iron', 'path' : 'assets/tile22.png', 'type' : 'resource' },
    23 : { 'name' : 'gold', 'path' : 'assets/tile23.png', 'type' : 'resource' },
    24 : { 'name' : 'coal', 'path' : 'assets/tile24.png', 'type' : 'resource' },
    25 : { 'name' : 'stick', 'path' : 'assets/tile25.png', 'type' : 'resource' },
}





