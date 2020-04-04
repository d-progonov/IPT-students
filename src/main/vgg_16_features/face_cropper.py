import cv2
import dlib


class FaceCropper:
    def __init__(self, type='cascade', file_name='./misc/haarcascade_frontalface_default.xml'):
        self.type = type
        if type == 'cascade':
            self.classifier = cv2.CascadeClassifier(file_name)
        elif type == 'dlib':
            self.shape_predictor = dlib.shape_predictor('./misc/shape_predictor_68_face_landmarks.dat')
            self.detector = dlib.get_frontal_face_detector()
        else:
            raise ValueError('Only cascade and dlib classifier is supported now!')

    def get_face_image(self, file_name):

        faces = []
        cv2_image = cv2.imread(file_name)
        # print(self.type)
        if self.type == 'cascade':
            grayed_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
            faces = self.classifier.detectMultiScale(image=grayed_image, scaleFactor=1.5, minNeighbors=5)
            print(faces)
        elif self.type == 'dlib':
            from skimage import io
            image = io.imread(file_name)
            dets_webcam = self.detector(image, 1)

            for k, d in enumerate(dets_webcam):
                # win2 = dlib.image_window()
                shape = self.shape_predictor(image, d)
                # win2.set_image(image)
                # win2.clear_overlay()
                # win2.add_overlay(d)
                # win2.wait_for_keypress('\n')
                # win2.add_overlay(shape)
                # win2.wait_for_keypress('\n')
                # print(d)
                coords = (d.left(), d.top(), d.right(), d.bottom())
                # print(coords)
                faces.append(coords)
        else:
            raise ValueError
        data = []
        if len(faces) == 0:
            return None
        for face in faces:
            if self.type == 'cascade':
                x, y, w, h = face
                cropped_image = cv2_image[y:y + h, x:x + w]
            elif self.type == 'dlib':
                x1, y1, x2, y2 = face
                cropped_image = cv2_image[y1:y2, x1:x2]
            else:
                raise ValueError
            return cropped_image
            # cv2.imshow("Cropped", cropped_image)
            # cv2.waitKey(0)

    def save_image(self, cv_image, file_name):
        cv2.imwrite(file_name, cv_image)
