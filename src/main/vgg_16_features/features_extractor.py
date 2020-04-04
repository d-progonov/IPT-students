from vggface import VGGFace
import utils
from keras.preprocessing import image
import numpy as np


class FeaturesExtractor:

    def __init__(self, input_shape=(224, 224, 3)):
        # take only 2 first parameters
        self.target_size = tuple(list(input_shape)[:2])
        # create model
        self.model = VGGFace(include_top=False, input_shape=input_shape)

    def extract_features(self, file_name):
        face_image = image.load_img(file_name, target_size=self.target_size)
        image_as_array = image.img_to_array(face_image)
        image_as_array = np.expand_dims(image_as_array, axis=0)
        image_as_array = utils.preprocess_input(image_as_array, version=1)
        return self.model.predict(image_as_array)
