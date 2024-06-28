from pygame import Vector2 as vector
from math import floor

from src.settings import *
import src.settings as settings


def isoToScreen(isoPos):
    isoX, isoY = isoPos
    screenX = (isoX + isoY) * settings.TILE_SIZE
    screenY = (isoX - isoY) * settings.TILE_SIZE / 2
    return vector(screenX, screenY) - vector(0, settings.TILE_SIZE//2)

def screenToIso(screenPos):
    screenX, screenY = screenPos
    isoX = screenY / settings.TILE_SIZE + screenX / (2*settings.TILE_SIZE)
    isoY = screenX / (2*settings.TILE_SIZE) - screenY / settings.TILE_SIZE 
    return floor(isoX), floor(isoY)

def rotate_90_clockwise(pos):
    x, y = pos
    return (y, -x)





    
