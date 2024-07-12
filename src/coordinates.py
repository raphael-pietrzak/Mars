from pygame import Vector2 as vector
from math import floor

from .settings import *
import settings as settings


def isoToScreen(isoPos):
    isoX, isoY = isoPos
    screenX = (isoX + isoY) * settings.TILE_SIZE
    screenY = (isoX - isoY) * settings.TILE_SIZE / 2
    return vector(screenX, screenY) 

def screenToIso(screenPos):
    screenX, screenY = screenPos + vector(settings.TILE_SIZE, 0)
    isoX = screenY / settings.TILE_SIZE + screenX / (2*settings.TILE_SIZE)
    isoY = screenX / (2*settings.TILE_SIZE) - screenY / settings.TILE_SIZE 
    return floor(isoX), floor(isoY)

def infiniteToAbs(infinitePos):
    x, y = infinitePos
    return x%settings.MAP_SIZE, y%settings.MAP_SIZE

def rotate_90_clockwise(pos):
    x, y = pos
    return (y, -x)





    
