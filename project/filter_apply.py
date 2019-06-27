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


def apply_dog_nose( image, nose ):
    (nose_x,nose_y,nose_width,nose_height) = nose
    print(parameters.MasksPaths.DogNoseDarkBackground)
    mask = cv2.imread(parameters.MasksPaths.DogNoseDarkBackground, cv2.IMREAD_COLOR)
    print("mask shape {}\n".format(mask.shape))
    reshaped_mask = cv2.resize(mask, (nose_width, nose_height))
    print(reshaped_mask.shape, mask.shape)

    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (0.5 * s_img[:, :, c] +
            alpha_l * l_img[y1:y2, x1:x2, c])

    return
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