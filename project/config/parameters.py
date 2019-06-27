from enum import Enum

IMG_DIR = '../imgs/'
MASK_DIR = '../masks'

class MasksPaths():
    Dog = MASK_DIR + '/dog/dog_mask.png'
    DogDarkBackground = MASK_DIR + '/dog/dog_mask_dark_background.png'
    DogNose = MASK_DIR + '/dog/dog_nose.png'
    DogNoseDarkBackground = MASK_DIR + '/dog/dog_nose_dark_background.png'
    
class Colors():
    Blue = (255,0,0)
    Green = (0,255,0)
    Red = (0,0,255)

class MaskTypes(Enum):
    Dog = 1