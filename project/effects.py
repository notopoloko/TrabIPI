import cv2
from config import parameters
import numpy as np


# definir logica de aplicacao de efeito
def applyEffectWithoutBackGround(image, faceRegion):
    # Retira a regiao da face e calcula a distancia 
    (face_x, face_y, face_width, face_height) = faceRegion
    white_image = 255*np.ones(shape = [image.shape[0], image.shape[1], 1], dtype=np.uint8)
    white_image[face_y:face_y + face_height, face_x:face_x + face_width] = np.zeros(shape = [face_height, face_width, 1], dtype=np.uint8)
    a = cv2.distanceTransform(white_image, cv2.DIST_L2, 5)
    a = cv2.normalize(a, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # print(image.shape,a.shape)
    # Multiplica cada elemento da imagem pelo seu peso correspondente
    image[:,:,0] = cv2.multiply(image[:,:,0], 1.0 - a, dtype=cv2.CV_8UC1)
    image[:,:,1] = cv2.multiply(image[:,:,1], 1.0 - a, dtype=cv2.CV_8UC1)
    image[:,:,2] = cv2.multiply(image[:,:,2], 1.0 - a, dtype=cv2.CV_8UC1)

    # Já possui um efeito bom aqui
    # print(image.max())
    # cv2.imshow('something',image)
    # cv2.waitKey(0)
    return image

def applyEffectWithBackGround(image, faceRegion, background):
    (face_x, face_y, face_width, face_height) = faceRegion
    white_image = 255*np.ones(shape = [image.shape[0], image.shape[1], 1], dtype=np.uint8)
    white_image[face_y:face_y + face_height, face_x:face_x + face_width] = np.zeros(shape = [face_height, face_width, 1], dtype=np.uint8)
    a = cv2.distanceTransform(white_image, cv2.DIST_L2, 5)
    a = cv2.normalize(a, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    image[:,:,0] = cv2.multiply(image[:,:,0], 1.0 - a, dtype=cv2.CV_8UC1)
    image[:,:,1] = cv2.multiply(image[:,:,1], 1.0 - a, dtype=cv2.CV_8UC1)
    image[:,:,2] = cv2.multiply(image[:,:,2], 1.0 - a, dtype=cv2.CV_8UC1)

    reshaped_background = cv2.resize(background,  (image.shape[1], image.shape[0]))
    # Controle do efeito de sera aplicada na image. Vai de 0 até 0.99
    controleEfeito = 0.1
    image[:,:,0] += cv2.multiply(reshaped_background[:,:,0], a - controleEfeito, dtype=cv2.CV_8UC1)
    image[:,:,1] += cv2.multiply(reshaped_background[:,:,1], a - controleEfeito, dtype=cv2.CV_8UC1)
    image[:,:,2] += cv2.multiply(reshaped_background[:,:,2], a - controleEfeito, dtype=cv2.CV_8UC1)

    return image

def applyBlurOutsideFace(image, faceRegion):
    (face_x, face_y, face_width, face_height) = faceRegion

    image[0: image.shape[0], 0:face_x] = cv2.blur(image[ 0: image.shape[0], 0:face_x ], (3,3))
    image[0: face_y, face_x: image.shape[1]] = cv2.blur(image[ 0: face_y, face_x: image.shape[1] ], (3,3))
    image[face_y+face_height: image.shape[0], face_x:image.shape[1]] = cv2.blur(image[ face_y+face_height: image.shape[0], face_x:image.shape[1] ], (3,3))
    image[face_y: face_y + face_height, face_x + face_width:image.shape[1] ] = cv2.blur(image[ face_y: face_y + face_height, face_x + face_width:image.shape[1] ], (3,3))

    # print(face_x, image.shape[0])
    return image

def applyBlurOutsideFace(image, faceRegion):
    (face_x, face_y, face_width, face_height) = faceRegion

    image[0: image.shape[0], 0:face_x] = cv2.blur(image[ 0: image.shape[0], 0:face_x ], (3,3))
    image[0: face_y, face_x: image.shape[1]] = cv2.blur(image[ 0: face_y, face_x: image.shape[1] ], (3,3))
    image[face_y+face_height: image.shape[0], face_x:image.shape[1]] = cv2.blur(image[ face_y+face_height: image.shape[0], face_x:image.shape[1] ], (3,3))
    image[face_y: face_y + face_height, face_x + face_width:image.shape[1] ] = cv2.blur(image[ face_y: face_y + face_height, face_x + face_width:image.shape[1] ], (3,3))

    # print(face_x, image.shape[0])
    return image

# def applyEnlargeEye(image, rEye, lEye):
#     (r_eye_x, r_eye_y, r_eye_width, r_eye_height) = rEye
#     (l_eye_x, l_eye_y, l_eye_width, l_eye_height) = lEye

#     image[]
#     return image

