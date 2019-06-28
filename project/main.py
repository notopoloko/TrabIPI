import cv2
import os
import math
from config import parameters
import filters


face_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_mcs_eyepair_big.xml')
nose_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_mcs_nose.xml')


if __name__ == '__main__':

    images_dataset = os.listdir(parameters.IMG_DIR)

    for img in images_dataset[:]:

        img_full_name = parameters.IMG_DIR + img;

        print("Reading image {}\n".format(img_full_name))
        colored_image = cv2.imread(img_full_name, cv2.IMREAD_COLOR)
        colored_image = cv2.resize(colored_image, None, fx=0.2,fy=0.15) 


        faces = face_cascade.detectMultiScale(colored_image, 1.1, 5) 
        for face_position in faces: 
            (face_x, face_y, face_width, face_height) = face_position
            cv2.rectangle(colored_image,(face_x, face_y),(face_x + face_width, face_y + face_height), parameters.Colors.Red, 2) 
            face_slot = colored_image[face_y:face_y + face_height, face_x:face_x + face_width] 
            
            eyes = eye_cascade.detectMultiScale(face_slot,1.1,4) 
            noses = nose_cascade.detectMultiScale(face_slot,1.3,4)

            if len(noses) != 0:
                best_nose = filters.select_best_nose_on_face(face_position,noses = noses)
            else:
                best_nose = None
            best_eyes = filters.select_best_eyes_on_face(eyes= eyes)
            # noseModified = filters.apply_dog_nose(best_nose)

            for eye_position in best_eyes:
                (eye_x,eye_y,eye_width,eye_height) = eye_position
                
                cv2.rectangle(colored_image,(face_x + eye_x ,face_y + eye_y),(face_x + eye_x +eye_width ,face_y + eye_y+eye_height),parameters.Colors.Blue,2) 

            
            try:
                (nose_x,nose_y,nose_width,nose_height) = best_nose
                print("best nose {}".format(best_nose))
                cv2.rectangle(colored_image,(face_x + nose_x ,face_y + nose_y),(face_x + nose_x +nose_width , face_y + nose_y+nose_height),parameters.Colors.Green,2) 
            except Exception as e:
                pass
            cv2.imshow('colored_image',colored_image) 
            cv2.waitKey(0)  
            try:
                result = colored_image.copy()

                # result = filters.apply_bread_face(result, face_position)
                result = filters.apply_glass(result, eye_position, face_position)
                result = filters.apply_dog_mask(result, best_nose, face_position)
                

            except Exception as e:
                print('deu ruim', e)
                result =  colored_image
            
        cv2.imshow('colored_image',result) 
        cv2.waitKey(0)



    cv2.destroyAllWindows()