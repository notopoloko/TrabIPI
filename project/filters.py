import numpy as np
import cv2
from config import parameters

def select_best_eyes_on_face(eyes):
    # TODO melhorar funcao
    try:
        return eyes[:2]
    except Exception as e:
        return eyes

def select_best_nose_on_face(noses):
    # TODO melhorar funcao
    try:
        return noses[:1][0]
    except Exception as e:
        return noses


def apply_dog_mask(image, best_nose, face_position):
   
    result_image = _apply_dog_nose(image, best_nose, face_position)
    
    return result_image



def _apply_dog_nose(image, best_nose, face_position):
    (nose_x,nose_y,nose_width,nose_height) = best_nose
    (face_x, face_y, face_width, face_height) = face_position

    result_image = image.copy()

    dog_nose = cv2.imread(parameters.MasksPaths.DogNose, cv2.IMREAD_COLOR)

    print((nose_width,nose_height),'teste')
    reshaped_nose= cv2.resize(dog_nose, (nose_width, nose_height ))
    print(reshaped_nose.shape,'teste')

    
    print("[image shape {}]chan {} to {} || row {} to {} || col {} to {}\n".format(reshaped_nose.shape, 0,image.shape[-1], 0, nose_width, 0, nose_height  ))
    print(face_x + nose_x , ",",face_x + nose_x + nose_width)        
    print(face_y + nose_y , ",",face_y + nose_y + nose_height)     
    
    for channel in range(0,image.shape[-1]):
        for row in range( 0,   nose_height):
            for col in range(0, nose_width ):
                # print('index {},{},{} \n'.format(row,col,channel))
                if reshaped_nose[row][col][channel] < 200:
                    result_image[face_y + nose_y + row ][face_x + nose_x  + col ][channel] = reshaped_nose[row][col][channel]
                else:
                    continue

    return result_image



# def apply_dog_nose( image, nose ):
#     (nose_x,nose_y,nose_width,nose_height) = nose
#     print(parameters.MasksPaths.DogNoseDarkBackground)
#     mask = cv2.imread(parameters.MasksPaths.DogNoseDarkBackground, cv2.IMREAD_COLOR)
#     print("mask shape {}\n".format(mask.shape))
#     reshaped_mask = cv2.resize(mask, (nose_width, nose_height))
#     print(reshaped_mask.shape, mask.shape)

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
        print(result.shape, image.shape, result.shape)

        # result = cv2.addWeighted(reshaped_mask, 0.5, image, 0.5, 0)

        # for i in range(result.shape[2]):
        #     for j in range(result.shape[0]):
        #         for k in range(result.shape[1]):
        #             if reshaped_mask[j][k][i] > 200:
        #                 result[j][k][i] = image[j][k][i]
        #             else:
        #                 result[j][k][i] = reshaped_mask[j][k][i]

    return result