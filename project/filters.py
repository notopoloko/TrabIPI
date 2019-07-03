import numpy as np
import cv2
from config import parameters
import math

def select_best_eyes_on_face(eyes):

        return eyes

def findBestTwoEyes (image_slot, eyes_cadidates):
    return eyes_cadidates


def _select_area_for_glasses(face_position, eyes):
    
    (eye_x,eye_y,eye_width,eye_height) = eyes

    previous_width = eye_width
    (face_x, face_y, face_width, face_height) = face_position

    eye_width = math.ceil(eye_width*1.2)
    eye_height = math.ceil(face_height*0.25)
    # eye_x = math.ceil(eye_width*0.1875)
    eye_x = eye_x - (eye_width//2  - previous_width//2)
    eye_y = math.ceil(eye_y*0.9)

    best_eye = [[eye_x,eye_y,eye_width,eye_height]]
    
    return best_eye

def select_best_nose_on_face(face_position,noses):
    best_nose = None

    try:
        best_nose = noses[:1][0]
    except Exception as e:
        best_nose
    
    (nose_x,nose_y,nose_width,nose_height) = best_nose
    (face_x, face_y, face_width, face_height) = face_position


    nose_width = face_width //2
    nose_x = math.ceil(face_width*0.25)

    best_nose = [nose_x,nose_y,nose_width,nose_height]
    return best_nose


def apply_glass(image, eye_position, face_position):
    (eye_x,eye_y,eye_width,eye_height) = eye_position
   
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    glasses = cv2.imread(parameters.MasksPaths.Glasses, cv2.IMREAD_COLOR)

    reshaped_glasses = cv2.resize(glasses, (eye_width, eye_height))

        
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   eye_height):
            for col in range(0, eye_width ):
                if reshaped_glasses[row][col][channel] < 230:
                    result_image[face_y + eye_y + row ][face_x + eye_x  + col ][channel] = reshaped_glasses[row][col][channel]
                else:
                    continue

    return result_image

def apply_flowers(image,  face_position, angle = 0):
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    flowers = cv2.imread(parameters.MasksPaths.Flowers, cv2.IMREAD_UNCHANGED)
    
    reshaped_flowers = cv2.resize(flowers, (face_width, face_height//2))
       
    rows, cols, _ = reshaped_flowers.shape
    M = cv2.getRotationMatrix2D ((cols/2, rows/2), (-angle*180/math.pi)*0.85, 1)
    reshaped_flowers = cv2.warpAffine(reshaped_flowers, M, (cols, rows))
    
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   face_height//2):
            for col in range(0, face_width ):
                if reshaped_flowers[row][col][3] > 240:
                    offset = face_height//6
                    result_image[ max(face_y  + row - offset , 0) ][ max(face_x   + col , 0) ][channel] = reshaped_flowers[row][col][channel]
                else:
                    continue

    return result_image


def apply_harry_potter_mask(image, eye_position, face_position, angle = 0):
    result_image = image.copy()
    try:
        result_image = _apply_hp_glasses(result_image, eye_position, face_position, angle)
    except Exception as e:  
        print('teste1')
    try:
        result_image = _apply_hp_thunder(result_image, eye_position, face_position)
    except Exception as e:  
        print('teste2')

    try:
        result_image = _apply_hp_scarf(result_image,  face_position)
    except Exception as e:  
        print('teste3')
        

    return result_image



def _apply_dog_ears(image,  face_position):
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    dog_ears = cv2.imread(parameters.MasksPaths.DogEars, cv2.IMREAD_UNCHANGED)
    
    reshaped_ears = cv2.resize(dog_ears, (face_width, face_height//3 ))

    for channel in range(0,image.shape[-1]):
        for row in range( 0,   face_height//3):
            for col in range(0, face_width ):
                if reshaped_ears[row][col][3] >250:
                    result_image[min(face_y  + row - (math.ceil(face_height*0.2)), image.shape[0]-1) ][min(face_x   + col , image.shape[1]-1) ][channel] = reshaped_ears[row][col][channel]
                else:
                    continue

    return result_image


def _apply_dog_nose(image, best_nose, face_position, angle = 0):
    (nose_x,nose_y,nose_width,nose_height) = best_nose  
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    dog_nose = cv2.imread(parameters.MasksPaths.DogNose, cv2.IMREAD_UNCHANGED)

    reshaped_nose= cv2.resize(dog_nose, (nose_width, nose_height ))

    rows, cols, _ = reshaped_nose.shape
    M = cv2.getRotationMatrix2D ((cols/2, rows/2), (-angle*180/math.pi)*0.85, 1)
    reshaped_nose = cv2.warpAffine(reshaped_nose, M, (cols, rows))

    
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   nose_height):
            for col in range(0, nose_width ):
                if reshaped_nose[row][col][3] > 250:
                    result_image[min(face_y + nose_y + row, image.shape[0]-1) ][min(face_x + nose_x  + col, image.shape[1]-1) ][channel] = reshaped_nose[row][col][channel]
                else:
                    continue

    return result_image



def apply_dog_mask(image, best_nose, face_position, angle = 0):
    result_image = image.copy()
    try:
      result_image = _apply_dog_ears(image,  face_position)
    except Exception as e:
        print(e)

    result_image = _apply_dog_nose(result_image, best_nose, face_position, angle)

    return result_image


def _apply_hp_glasses(image, eye_position, face_position, angle ):
    
    (eye_x,eye_y,eye_width,eye_height) = _select_area_for_glasses(face_position, eye_position)[0]
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    hp = cv2.imread(parameters.MasksPaths.Hp, cv2.IMREAD_UNCHANGED)

    reshaped_hp_glasses = cv2.resize(hp, (eye_width, eye_height ))

    rows, cols, _ = reshaped_hp_glasses.shape
    M = cv2.getRotationMatrix2D ((cols/2, rows/2), (-angle*180/math.pi)*0.85, 1)
    reshaped_hp_glasses = cv2.warpAffine(reshaped_hp_glasses, M, (cols, rows))

    
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   eye_height):
            for col in range(0, eye_width ):
                if reshaped_hp_glasses[row][col][3] >230:
                    result_image[min(face_y + eye_y + row, image.shape[0]-1) ][min(face_x + eye_x  + col, image.shape[1]-1) ][channel] = reshaped_hp_glasses[row][col][channel]
                else:
                    continue

    return result_image

def _apply_hp_thunder(image, eye_position, face_position):
    (eye_x,eye_y,eye_width,eye_height) = eye_position
    (face_x, face_y, face_width, face_height) = face_position

    hp_thunder_width = eye_width//3
    hp_thunder_height = math.ceil(eye_height*0.8)
    hp_thunder_x = eye_x
    hp_thunder_y =  eye_y //3
    result_image = image.copy()

    hp_thunder = cv2.imread(parameters.MasksPaths.HpThunder, cv2.IMREAD_UNCHANGED)

    reshaped_thunder = cv2.resize(hp_thunder, (hp_thunder_width, hp_thunder_height ))

    for channel in range(0,image.shape[-1]):
        for row in range( 0,   hp_thunder_height):
            for col in range(0, hp_thunder_width ):
                if reshaped_thunder[row][col][3] >230:
                    result_image[min(face_y + hp_thunder_y + row, image.shape[0]-1)][min(face_x + hp_thunder_x  + col, image.shape[1]-1) ][channel] = reshaped_thunder[row][col][channel]
                else:
                    continue

    return result_image



def _apply_hp_scarf(image,  face_position):
    (face_x, face_y, face_width, face_height) = face_position
    face_y = min (face_y + face_width, image.shape[1])
    result_image = image.copy()
    
    hp_scarf= cv2.imread(parameters.MasksPaths.HpScarf, cv2.IMREAD_UNCHANGED)
    
    face_width = math.ceil(face_width*1.2)
    reshaped_hp_scarf = cv2.resize(hp_scarf, (face_width, face_height ))

    for channel in range(0,image.shape[-1]):
        for row in range( 0,   face_height):
            for col in range(0, face_width ):
                if reshaped_hp_scarf[row][col][3] >250:
                    
                    result_image[min(face_y  + row - (math.ceil(face_height*0.2)),image.shape[0]-1) ][min(face_x   + col ,image.shape[1]-1) ][channel] = reshaped_hp_scarf[row][col][channel]
                else:
                    continue

    return result_image


