import cv2
import os
import math
from config import parameters
import filters
import effects


face_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_mcs_eyepair_big.xml')
two_eye_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_eye.xml')

nose_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_mcs_nose.xml')


if __name__ == '__main__':

    images_dataset = os.listdir(parameters.IMG_DIR)

    for img in images_dataset[1:2]:

        img_full_name = parameters.IMG_DIR + img

        print("Reading image {}\n".format(img_full_name))
        colored_image = cv2.imread(img_full_name, cv2.IMREAD_COLOR)
        colored_image = cv2.resize(colored_image, None, fx=0.2,fy=0.15) 

        faces = face_cascade.detectMultiScale(colored_image, 1.1, 5) 
        print( faces )
        for face_position in faces: 
            (face_x, face_y, face_width, face_height) = face_position
            # cv2.rectangle(colored_image,(face_x, face_y),(face_x + face_width, face_y + face_height), parameters.Colors.Red, 2) 
            face_slot = colored_image[face_y:face_y + face_height, face_x:face_x + face_width] 
            
            eyes = eye_cascade.detectMultiScale(face_slot,1.1,4) 
            noses = nose_cascade.detectMultiScale(face_slot,1.3,4)
            
            t_eye = two_eye_cascade.detectMultiScale(face_slot, 1.3, 5)
            # l_eye = left_eye.detectMultiScale(face_slot, 1.1, 4)
            angle = 0
            if (len(t_eye) == 2):
                t_eye = filters.findBestTwoEyes(face_slot, t_eye)
                (r_eye_x, r_eye_y, r_eye_width, r_eye_height) = t_eye[1]
                (l_eye_x, l_eye_y, l_eye_width, l_eye_height) = t_eye[0]

                # cv2.rectangle(colored_image,(face_x + l_eye_x ,face_y + l_eye_y),(face_x + l_eye_x + l_eye_width ,face_y + l_eye_y+l_eye_height),parameters.Colors.Black,2) 
                # cv2.rectangle(colored_image,(face_x + r_eye_x ,face_y + r_eye_y),(face_x + r_eye_x + r_eye_width ,face_y + r_eye_y+r_eye_height),parameters.Colors.Black,2) 

                angle = math.atan( (r_eye_y + r_eye_height//2 - l_eye_y - l_eye_height//2 ) / (r_eye_x + r_eye_width//2 - l_eye_x - l_eye_width//2 ) )
                print('Good angle finded: ', '{0:.2f} graus'.format(angle * 180 / math.pi))

            if len(noses) != 0:
                best_nose = filters.select_best_nose_on_face(face_position,noses = noses)
            else:
                best_nose = None
            best_eyes = filters.select_best_eyes_on_face(eyes= eyes)
            # noseModified = filters.apply_dog_nose(best_nose)

            for eye_position in best_eyes:
                (eye_x,eye_y,eye_width,eye_height) = eye_position
                
                # cv2.rectangle(colored_image,(face_x + eye_x ,face_y + eye_y),(face_x + eye_x +eye_width ,face_y + eye_y+eye_height),parameters.Colors.Blue,2) 

            try:
                (nose_x,nose_y,nose_width,nose_height) = best_nose
                print("best nose {}".format(best_nose))
                # cv2.rectangle(colored_image,(face_x + nose_x ,face_y + nose_y),(face_x + nose_x +nose_width , face_y + nose_y+nose_height),parameters.Colors.Green,2) 
            except Exception as e:
                pass
            # cv2.imshow('colored_image',colored_image) 
            # cv2.waitKey(0)
            try:
                result = colored_image.copy()

                result = filters.apply_flowers(result, face_position, angle)
                result = effects.applyEffectWithoutBackGround(result, face_position)
                cv2.imshow('Sem background',result)
                cv2.waitKey(0)

                pink_background = cv2.imread(parameters.MasksPaths.PinkGradient, cv2.IMREAD_COLOR)
                result = effects.applyEffectWithBackGround(result, face_position, pink_background)
                cv2.imshow('Com background',result)
                cv2.waitKey(0)
                # result = filters.apply_glass(result, eye_position, face_position)
                # result = filters.apply_dog_mask(result, best_nose, face_position, angle)
                

            except Exception as e:
                print('deu ruim', e)
                result =  colored_image
            
        # cv2.waitKey(0)



    cv2.destroyAllWindows()