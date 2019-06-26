import cv2
import os
import math
from config import parameters
import filter_apply


face_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('../opencv/haarcascades/haarcascade_eye.xml')
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
            (x,y,width,height) = face_position
            cv2.rectangle(colored_image,(x,y),(x+width,y+height),parameters.Colors.Red,2) 
            face_slot = colored_image[y:y+height, x:x+width] 
            eyes = eye_cascade.detectMultiScale(face_slot,1.1,4) 
            noses = nose_cascade.detectMultiScale(face_slot,1.3,4)

            best_nose = filter_apply.select_best_nose_on_face(noses = noses)
            best_eyes = filter_apply.select_best_eyes_on_face(eyes= eyes);


            for eye_position in best_eyes:
                (eye_x,eye_y,eye_width,eye_height) = eye_position
                
                cv2.rectangle(face_slot,(eye_x ,eye_y),(eye_x +eye_width ,eye_y+eye_height),parameters.Colors.Blue,2) 
            
            for nose_position in best_nose:
                (nose_x,nose_y,nose_width,nose_height) = nose_position
                cv2.rectangle(face_slot,(nose_x ,nose_y),(nose_x +nose_width ,nose_y+nose_height),parameters.Colors.Green,2) 

            result = filter_apply.set_mask(face_slot, parameters.MaskTypes.Dog)
        cv2.imshow('colored_image',result) 
        cv2.waitKey(0)



    cv2.destroyAllWindows()