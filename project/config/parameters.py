from enum import Enum

IMG_DIR = '../imgs/'
MASK_DIR = '../masks'

class Colors():
    Blue = (255,0,0)
    Green = (0,255,0)
    Red = (0,0,255)

class MaskTypes(Enum):
    Dog = 1