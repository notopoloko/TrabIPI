from enum import Enum

IMG_DIR = '../imgs/'
MASK_DIR = '../masks'

class MasksPaths():
    Dog = MASK_DIR + '/dog/dog_mask.png'
    DogNose = MASK_DIR + '/dog/dog_nose4.png'
    DogEars= MASK_DIR + '/dog/dog_ears4.png'
    Glasses = MASK_DIR + '/glasses/glasses.png'
    BreadFace = MASK_DIR + '/bread/bread_face.png'
    Flowers = MASK_DIR + '/flowers/flowers.png'
    PinkGradient = MASK_DIR + '/flowers/pink_background.png'
    
class Colors():
    Blue = (255,0,0)
    Green = (0,255,0)
    Red = (0,0,255)
    Black = (0,0,0)

class MaskTypes(Enum):
    Dog = 1