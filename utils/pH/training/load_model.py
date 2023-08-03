import csv
import numpy as np
import pandas as pd
import os.path
import tensorflow as tf
import sys
import glob

from keras.layers import Dense
from keras.models import Model
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from tensorflow.keras.optimizers import SGD
from tensorflow import keras

# The images from the pH medium dataset will be resized
# to these dimensions in order to use pre-trained weights
WIDTH=224
HEIGHT=224

def create_data_list(images):
	data = []
	for img in images:
		basename = os.path.basename(img)
		tokens = basename.split("_")
		ph = float(tokens[3])
		data.append([str(img), ph])
	return data


ROOT_DATASET_DIR = "pH_medium_dataset"
test_images_path = ROOT_DATASET_DIR + "/" + "test/*.png"
test_images = glob.glob(test_images_path)
test_data = create_data_list(test_images)
test_df = pd.DataFrame(test_data, columns=['Filepath', 'ph'])

test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)

test_dataset = test_generator.flow_from_dataframe(
    dataframe=test_df,
    x_col='Filepath',
    y_col='ph',
    target_size=(WIDTH, HEIGHT),
    color_mode='rgb',
    class_mode='raw',
    batch_size=32,
    shuffle=False
)


model = keras.models.load_model('weights_ph_prediction.h5')
predicted_ph_values = np.squeeze(model.predict(test_dataset))
true_ph_values = test_dataset.labels

outfile = "PH.csv"
print(len(true_ph_values))
with open(outfile, 'w') as f:
	header = ['True pH', 'Predicted pH']
	writer = csv.writer(f)
	writer.writerow(header)
	for i in range(0, len(true_ph_values)):
		data = [true_ph_values[i], predicted_ph_values[i]]
		writer.writerow(data)
		print("True pH:", true_ph_values[i], "    Predicted:", predicted_ph_values[i])

print("Finish...")
