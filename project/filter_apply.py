import numpy as np
import cv2
from config import parameters

def select_best_eyes_on_face(eyes):
    # TODO melhorar funcao

    return eyes[:2];

def select_best_nose_on_face(noses):
    # TODO melhorar funcao
    return noses[:1]
def set_mask(image, mask_type):
    result = None

    if mask_type == parameters.MaskTypes.Dog:
        # TODO resize nas masks e colocar em cima
        result = image


    return result