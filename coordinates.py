from math import floor
from settings import *
from pygame import Vector2 as vector



def isoToScreen(isoPos):
    isoX, isoY = isoPos
    screenX = (isoX + isoY) * TILE_SIZE
    screenY = (isoX - isoY) * TILE_SIZE / 2
    return vector(screenX, screenY) - vector(0, TILE_SIZE//2)

def screenToIso(screenPos):
    screenX, screenY = screenPos
    isoX = screenY / TILE_SIZE + screenX / (2*TILE_SIZE)
    isoY = screenX / (2*TILE_SIZE) - screenY / TILE_SIZE 
    return floor(isoX), floor(isoY)



    
