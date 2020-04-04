from face_cropper import FaceCropper
from main import get_picked_images
import cv2, numpy as np


def test_contrast():
    img = cv2.imread('./face_1.png', 0)
    brt = 0
    img[img < 255 - brt] += brt
    cv2.imwrite('test.png', img)
if __name__ == '__main__':
    image = get_picked_images()[1]
    cascade_cropper = FaceCropper()
    dlib_cropper = FaceCropper('dlib')
    file_name = f'../lfw/lfw_picked/{image}'
    cimage, dimage = cascade_cropper.get_face_image(file_name), dlib_cropper.get_face_image(file_name)
    cascade_cropper.save_image(cimage, './cascade.jpg')
    cascade_cropper.save_image(dimage, './dlib.jpg')
    # print(cascade_cropper.get_face_image(file_name))
    # print(dlib_cropper.get_face_image(file_name))

