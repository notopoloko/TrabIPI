import cv2
from config import parameters
import numpy as np

# definir logica de aplicacao de efeito
def applyEffect(image, faceRegion):
    (face_x, face_y, face_width, face_height) = faceRegion

    white_image = 255*np.ones(shape = [image.shape[0], image.shape[1], 1], dtype=np.uint8)

    white_image[face_y:face_y + face_height, face_x:face_x + face_width] = np.zeros(shape = [face_height, face_width, 1], dtype=np.uint8)

    a = cv2.distanceTransform(white_image, cv2.DIST_L2, 5)
    # a = cv2.normalize(a, 0, 1., cv2.NORM_MINMAX)

    cv2.imshow('something',a)
    cv2.waitKey(0)

    pink_background = cv2.imread(parameters.MasksPaths.PinkGradient, cv2.IMREAD_COLOR)

    reshaped_pink_background = cv2.resize(pink_background,  (image.shape[1], image.shape[0]))

    result_image = cv2.addWeighted(image, 0.6, reshaped_pink_background, 0.4, 0)
    return result_image