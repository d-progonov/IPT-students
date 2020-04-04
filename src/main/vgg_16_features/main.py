from features_extractor import FeaturesExtractor
import os
from face_cropper import FaceCropper
import numpy as np

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Flatten, Dense, Input, Conv2D, Dropout


def get_files(path, allowed_extensions):
    path = os.path.abspath(path)
    if isinstance(allowed_extensions, list) or isinstance(allowed_extensions, str):
        allowed_extensions = tuple(allowed_extensions)
    elif not isinstance(allowed_extensions, tuple):
        raise ValueError('allowed_extension have to be tuple or array!')
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return [f for f in all_files if f.endswith(allowed_extensions)]

def get_picked_images():
    return get_files('../lfw/lfw_picked', 'jpg')

def crop_and_save_images(type = 'cascade'):
    if type in ('cascade', 'dlib'):
        cropper = FaceCropper(type)
    else:
        raise ValueError('Only cascade and dlib are supported now')
    file_to_save_pattern = '../lfw/lfw_picked_faces/{0}/{1}'
    file_to_get_pattern = '../lfw/lfw_picked/{0}'
    for image in get_picked_images():
        file_name = file_to_get_pattern.format(image)
        print(f'Detecting face in {file_name}')
        cropped_image = cropper.get_face_image(file_name)
        if cropped_image is None:
            print(f'No face was found in {file_name}')
        else:
            file_to_save = file_to_save_pattern.format(type, image)
            print(f'Face was identified. Saving image to {file_to_save}')
            cropper.save_image(cropped_image, file_to_save)

def extract_photo_features(extractor : FeaturesExtractor, source_path : str, destination_path: str, override : bool = False):
    if not os.path.exists(source_path):
        print(f'File {source_path} does not exists!')
        raise FileNotFoundError
    if os.path.exists(destination_path):
        message = f'{destination_path} already exists, ' + 'deleting' if override else 'skipping'
        print(message)
        if not override:
            return
        else:
            os.remove(destination_path)
    print(f'Extracting features from {source_path}')
    features = extractor.extract_features(source_path)
    print(f'Saving features to {destination_path}')
    np.save(destination_path, features)
    

def extract_features(path = '..\lfw_sorted', source_path = '.\\features_result'):
    directories = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    extractor = FeaturesExtractor()

    for dir in directories:
        files = [os.path.join(path, dir, d) for d in get_files(os.path.join(path, dir), ['jpg', 'png', 'jpeg', 'bmp'])]
        first_file = files[0]
        print(f'First file is {first_file}')
        etalon_dir_name = os.path.join(source_path, '.etalon')
        if not os.path.exists(etalon_dir_name):
            os.mkdir(etalon_dir_name)
        target_path = os.path.join(etalon_dir_name, dir + '.npy')
        print('ETALON FEATURES EXTRACTING STARTED')
        extract_photo_features(extractor, first_file, target_path)
        
        print('OTHER FEATURES EXTRACTING STARTED')
        other_files = files[1:]
        other_files__folder_path = os.path.join(source_path, dir)

        if not os.path.exists(other_files__folder_path):
            print(f'Creating directory {other_files__folder_path}')
            os.mkdir(other_files__folder_path)
        
        # counter = 1
        for file in other_files:
            print()
            # counter += 1
            # number = file.split('_')[-1].replace('0', '')
            # file_name = (number if number.isdigit() else str(counter)) + '.npy'
            file_name = os.path.splitext(os.path.basename(file))[0] + '.npy'
            target_file_path = os.path.join(other_files__folder_path, file_name)
            extract_photo_features(extractor, file, target_file_path)  

def get_model_and_name():
    model = Sequential()
    model.add(Conv2D(64, (3, 3),
                    input_shape=(7, 7, 512), padding='same',))
    # now: model.output_shape == (None, 64, 32, 32)

    model.add(Flatten())
    model.add(Dense(100, activation = 'relu'))
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(100, activation = 'relu'))
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(1, activation = 'sigmoid'))
    # now: model.output_shape == (None, 65536)
    return (model, 'test_flatten')

def get_data(file_name : str):
    features = np.load(file_name)[0]
    
def calculate_far_and_frr(model, model_name: str):
    
    pass

# TODO: Investigate possible types of faces extraction (Diploma)
# TODO: FAR and FRR with existing data and methods (Kursach)
if __name__ == '__main__':
    # extracting features 
    # extract_features('..\lfw_sorted', '..\\features_result')
    model, name = get_model_and_name()
    model.compile(loss='binary_crossentropy', optimizer = 'adam', metrics=['accuracy'])
    model.summary()

    #TODO: That
    #calculate_far_and_frr(model, name)

    pass
