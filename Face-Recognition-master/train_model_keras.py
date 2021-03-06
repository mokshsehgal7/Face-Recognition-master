import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.python.keras.utils import np_utils
import pydot
import graphviz

from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
import tensorflow.keras.utils
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import backend as K
import numpy as np
import pickle, os
K.set_image_data_format('channels_first')

def get_num_of_faces():
	return len(os.listdir('faces/'))

def mlp_model():
	num_of_faces = get_num_of_faces()
	model = Sequential()
	model.add(Dense(128, input_shape=(128, ), activation='relu'))
	model.add(Dropout(0.8))
	model.add(Dense(256, activation='relu'))
	model.add(Dropout(0.8))
	#model.add(Dense(1024, activation='relu'))
	#model.add(Dropout(0.8))
	model.add(Dense(num_of_faces, activation='softmax'))
	sgd = optimizers.SGD(lr=1e-2)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
	filepath="mlp_model_keras2.h5"
	checkpoint1 = ModelCheckpoint(filepath, monitor='accuracy', verbose=1, save_best_only=True, mode='max')
	callbacks_list = [checkpoint1]
	# from tensorflow.keras.utils import plot_model
	tf.keras.utils.plot_model(model, to_file='model.png', show_shapes=True)
	return model, callbacks_list

def train():
	with open("train_features", "rb") as f:
		train_images = np.array(pickle.load(f))
	with open("train_labels", "rb") as f:
		train_labels = np.array(pickle.load(f), dtype=np.int32)

	with open("test_features", "rb") as f:
		test_images = np.array(pickle.load(f))
	with open("test_labels", "rb") as f:
		test_labels = np.array(pickle.load(f), dtype=np.int32)

	train_labels = np_utils.to_categorical(train_labels)
	test_labels = np_utils.to_categorical(test_labels)
	model, callbacks_list = mlp_model()
	model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=400, batch_size=50, callbacks=callbacks_list)
	scores = model.evaluate(test_images, test_labels, verbose=3)
	print(scores)
	print("MLP Error: %.2f%%" % (100-scores[1]*100))
	model.save('cnn_model_keras2.h5')

train()