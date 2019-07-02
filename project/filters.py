import numpy as np
import cv2
from config import parameters
import math

def select_best_eyes_on_face(eyes):
    # TODO melhorar funcao
    try:
        return eyes[:2]
    except Exception as e:
        return eyes

def findBestTwoEyes (image_slot, eyes_cadidates):
    return eyes_cadidates

def select_best_nose_on_face(face_position,noses):
    best_nose = None

    try:
        best_nose = noses[:1][0]
    except Exception as e:
        best_nose
    
    (nose_x,nose_y,nose_width,nose_height) = best_nose
    (face_x, face_y, face_width, face_height) = face_position


    nose_width = face_width //2
    print("face width {} nose width {}\n".format(face_width, nose_width))
    nose_x = math.ceil(face_width*0.25)

    best_nose = [nose_x,nose_y,nose_width,nose_height]
    return best_nose


def apply_glass(image, eye_position, face_position):
    (eye_x,eye_y,eye_width,eye_height) = eye_position
   
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    glasses = cv2.imread(parameters.MasksPaths.Glasses, cv2.IMREAD_COLOR)

    reshaped_glasses = cv2.resize(glasses, (eye_width, eye_height))

        
    # print(face_y)
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   eye_height):
            for col in range(0, eye_width ):
                # # print('index {},{},{} \n'.format(row,col,channel))
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
    
    # print(face_y)
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   face_height//2):
            for col in range(0, face_width ):
                # # print('index {},{},{} \n'.format(row,col,channel))
                if reshaped_flowers[row][col][3] > 240:
                    offset = face_height//6
                    result_image[ max(face_y  + row - offset , 0) ][ max(face_x   + col , 0) ][channel] = reshaped_flowers[row][col][channel]
                else:
                    continue

    return result_image


def apply_dog_mask(image, best_nose, face_position, angle = 0):
    result_image = image.copy()
    try:
      result_image = _apply_dog_ears(result_image,  face_position)
    except Exception as e:
        print(e)

    result_image = _apply_dog_nose(result_image, best_nose, face_position, angle)

    return result_image



def _apply_dog_ears(image,  face_position):
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    dog_ears = cv2.imread(parameters.MasksPaths.DogEars, cv2.IMREAD_UNCHANGED)
    
    reshaped_ears = cv2.resize(dog_ears, (face_width, face_height//3 ))

    # print(face_y)
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   face_height//3):
            for col in range(0, face_width ):
                # # print('index {},{},{} \n'.format(row,col,channel))
                if reshaped_ears[row][col][3] >250:
                    result_image[max(face_y  + row - (math.ceil(face_height*0.2)),0) ][max(face_x   + col ,0) ][channel] = reshaped_ears[row][col][channel]
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

    # print("[image shape {}]chan {} to {} || row {} to {} || col {} to {}\n".format(reshaped_nose.shape, 0,image.shape[-1], 0, nose_width, 0, nose_height  ))
    # print(face_x + nose_x , ",",face_x + nose_x + nose_width)        
    # print(face_y + nose_y , ",",face_y + nose_y + nose_height)     
    
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   nose_height):
            for col in range(0, nose_width ):
                # # print('index {},{},{} \n'.format(row,col,channel))
                if reshaped_nose[row][col][3] > 250:
                    result_image[face_y + nose_y + row ][face_x + nose_x  + col ][channel] = reshaped_nose[row][col][channel]
                else:
                    continue

    return result_image



# def apply_dog_nose( image, nose ):
#     (nose_x,nose_y,nose_width,nose_height) = nose
# #     print(parameters.MasksPaths.DogNoseDarkBackground)
#     mask = cv2.imread(parameters.MasksPaths.DogNoseDarkBackground, cv2.IMREAD_COLOR)
# #     print("mask shape {}\n".format(mask.shape))
#     reshaped_mask = cv2.resize(mask, (nose_width, nose_height))
# #     print(reshaped_mask.shape, mask.shape)

#     for c in range(0, 3):
#         image[y1:y2, x1:x2, c] = (0.5 * s_img[:, :, c] +
#             alpha_l * l_img[y1:y2, x1:x2, c])

#     return
def set_mask(image, mask_type):
    reshaped_mask =  None
    result = np.zeros(image.shape)


    mask = cv2.imread(parameters.MasksPaths.Dog, cv2.IMREAD_COLOR)
    if mask_type == parameters.MaskTypes.Dog:
        # TODO resize nas masks e colocar em cima
        reshaped_mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        # print(result.shape, image.shape, result.shape)

        # result = cv2.addWeighted(reshaped_mask, 0.5, image, 0.5, 0)

        # for i in range(result.shape[2]):
        #     for j in range(result.shape[0]):
        #         for k in range(result.shape[1]):
        #             if reshaped_mask[j][k][i] > 200:
        #                 result[j][k][i] = image[j][k][i]
        #             else:
        #                 result[j][k][i] = reshaped_mask[j][k][i]

    return result
