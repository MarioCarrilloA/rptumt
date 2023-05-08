import csv
import glob
import numpy as np
import os.path
import pandas as pd
import sys
import tensorflow as tf

from keras.layers import Dense
from keras.models import Model
from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import SGD

# The images from the pH medium dataset will be resized
# to these dimensions in order to use pre-trained weights
WIDTH=224
HEIGHT=224

# This function read the images from the directory dataset.
# The pH values is included in the name of the image, therefore
# it is necessary to parse that information.
def create_data_list(images):
	data = []
	for img in images:
		basename = os.path.basename(img)
		tokens = basename.split("_")
		ph = float(tokens[3])
		data.append([str(img), ph])
	return data

# Specify paths to read images from dataset
ROOT_DATASET_DIR = "pH_medium_dataset"
train_images_path = ROOT_DATASET_DIR + "/" + "train/*.png"
test_images_path = ROOT_DATASET_DIR + "/" + "test/*.png"
validation_images_path = ROOT_DATASET_DIR + "/" + "validation/*.png"

train_images = glob.glob(train_images_path)
test_images = glob.glob(test_images_path)
validation_images = glob.glob(validation_images_path)

# Read information from dataset directory
train_data = create_data_list(train_images)
test_data = create_data_list(test_images)
validation_data = create_data_list(validation_images)

# Create data frames
train_df = pd.DataFrame(train_data, columns=['Filepath', 'ph'])
test_df = pd.DataFrame(test_data, columns=['Filepath', 'ph'])
validation_df = pd.DataFrame(validation_data, columns=['Filepath', 'ph'])

# Configure data
train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)

test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)

validation_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)

train_dataset = train_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='ph',
    target_size=(WIDTH, HEIGHT),
    color_mode='rgb',
    class_mode='raw',
    batch_size=32,
    shuffle=True,
    seed=42
)

validation_dataset = validation_generator.flow_from_dataframe(
    dataframe=validation_df,
    x_col='Filepath',
    y_col='ph',
    target_size=(WIDTH, HEIGHT),
    color_mode='rgb',
    class_mode='raw',
    batch_size=32,
    shuffle=True,
    seed=42
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


print("Init VGG16")
inputs = tf.keras.Input(shape=(WIDTH, HEIGHT, 3))
base_model = tf.keras.applications.VGG16(
    include_top=False,
    weights=None,
    input_shape=(WIDTH, HEIGHT, 3)
)

# remove the final fully connected layer
base_model.layers.pop()

x = tf.keras.layers.Flatten()(base_model.output)
x = Dense(1)(x)
model = Model(inputs=base_model.input, outputs=x)


# Configure SGD as optimization algorithm
model.compile(
    optimizer=SGD(learning_rate=0.001, momentum=0.9),
    loss='mse'
)

# Early stopping as algorithm to stop training
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

print("Start training!!!")
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=100,
    callbacks=[callback]
)

# Get true and predicted pH values
predicted_ph_values = np.squeeze(model.predict(test_dataset))
true_ph_values = test_dataset.labels

print("Evaluate")
print(model.evaluate(test_dataset))
print("-------------------------------------------")
print(model.evaluate(test_dataset, verbose=0))
print("-------------------------------------------")
print("Summar")
print(model.summary())
print("-------------------------------------------")

# Save model in HDF5 format
print("Save model")
model.save('weights_ph_prediction.h5')


# Save true values and prediction
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
