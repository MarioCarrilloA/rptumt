import csv
import numpy as np
import pandas as pd
import os.path
import tensorflow as tf
import sys
import glob
import time

from tensorflow import keras

# The images from the pH medium dataset will be resized
# to these dimensions in order to use pre-trained weights
WIDTH=224
HEIGHT=224


def create_data_list(img):
    data = []
    basename = os.path.basename(img)
    tokens = basename.split("_")
    ph = float(tokens[3])
    data.append([str(img), ph])

    return data

preprocess = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)


# Starting time - total performance time after to load
# python modules dependencies
st_total = time.time()

# Get start and end time of the model loading
st_load_model = time.time()
model = keras.models.load_model('weights_ph_prediction.h5')
et_load_load = time.time()

# Read 20 PNG images and process them one per one
processing_time = []
images_paths = glob.glob("validation/*.png")
for img in images_paths:
    st_process = time.time()

    # Load data
    data = create_data_list(img)
    single_image_df = pd.DataFrame(data, columns=['Filepath', 'ph'])

    # Preprocess image
    sample = preprocess.flow_from_dataframe(
        dataframe=single_image_df,
        x_col='Filepath',
        y_col='ph',
        target_size=(WIDTH, HEIGHT),
        color_mode='rgb',
        class_mode='raw',
    )
    predicted_ph_value = np.squeeze(model.predict(sample))
    et_process = time.time()
    pt = et_process - st_process
    # Accumalate the prediction time per samples to compute
    # the average time
    processing_time.append(pt)    

    # Show results
    #true_ph_value = sample.labels
    #print("Ground truth:{0},  Predicted:{1}".format(true_ph_value, predicted_ph_value))

# Capture the end of the moment when all images were processed
et_total = time.time()

# Measure latencies
loading_model_time = et_load_model - st_load_model
total_proces_time = et_total - st_total
avg_process_time_per_image = sum(processing_time) / len(processing_time)

print("Model loading time:", et_load - st_load)
print("AVG process time per image:", avg_time_per_image)
print("Total process time:", et_total - st_total)

