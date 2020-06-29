# -*- coding: utf-8 -*-
"""FashionMNIST_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XSgw5_5etT5XfMq4i0W0uVlC3ZOc1Og5
"""

# Importing libraries
import numpy as np
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D,Dense,MaxPooling2D,Dropout,Flatten, Activation, BatchNormalization,LeakyReLU
import matplotlib.pyplot as plt

# Loading Dataset
def load_dataset():
	# load dataset
	(trainX, trainY), (testX, testY) = fashion_mnist.load_data()
	# reshape dataset to have a single channel
	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))
	# one hot encode target values
	trainY = to_categorical(trainY)
	testY = to_categorical(testY)
	return trainX, trainY, testX, testY

# Preparing Pixel Data
def prep_pixels(trainX, testX):
  # scale pixels
  # convert from integers to floats
  trainX = trainX.astype('float32')
  testX = testX.astype('float32')
  #Centering pixels
  trainX -= np.mean(trainX, axis=0)
  testX -= np.mean(testX, axis=0)
  return trainX, testX

# Implementing the model
BS = 64
EPOCHS = 10
NUM_TOPICS = 10
DROP_RATE = 0.25
def build_model(trainX, trainY,batch_size,epochs, num_topics, drop_rate):
  model = Sequential()

  model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(28,28,1),padding='same'))
  model.add(BatchNormalization())
  model.add(Conv2D(32, (3, 3), activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
  model.add(Dropout(DROP_RATE))

  model.add(Conv2D(64, kernel_size=(3, 3),activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(Conv2D(64, (3, 3), activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
  model.add(Dropout(DROP_RATE))

  model.add(Conv2D(128, kernel_size=(3, 3),activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(Conv2D(128, (3, 3), activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
  model.add(Dropout(DROP_RATE))

  model.add(Conv2D(256, kernel_size=(3, 3),activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(Conv2D(256, (3, 3), activation='relu',padding='same'))
  model.add(BatchNormalization())
  model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
  model.add(Dropout(DROP_RATE))

  model.add(Flatten())
  model.add(Dense(500,use_bias=False,activation='relu'))
  model.add(BatchNormalization())
  model.add(Dropout(DROP_RATE)) 
  model.add(Dense(NUM_TOPICS, activation='softmax'))
  
  # Compile the model
  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
  # Train the model
  history = model.fit(trainX, trainY, epochs=EPOCHS, batch_size=BS, validation_data=(testX, testY),shuffle=True)
  score = model.evaluate(testX, testY, verbose=0)
  return score ,history

def curves(fashion_train):
  accuracy = fashion_train.history['accuracy']
  val_accuracy = fashion_train.history['val_accuracy']
  loss = fashion_train.history['loss']
  val_loss = fashion_train.history['val_loss']
  epochs = range(len(accuracy))
  # Plots
  plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
  plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
  plt.title('Training and validation accuracy')
  plt.legend()
  plt.figure()
  plt.plot(epochs, loss, 'bo', label='Training loss')
  plt.plot(epochs, val_loss, 'b', label='Validation loss')
  plt.title('Training and validation loss')
  plt.legend()
  plt.show()

# loading the dataset
trainX, trainY, testX, testY = load_dataset()
# preparing pixel data
trainX, testX = prep_pixels(trainX, testX)
# evaluating the model
scores, histories = build_model(trainX, trainY, BS, EPOCHS, NUM_TOPICS, DROP_RATE)

# learning curves
curves(histories)

print('Accuracy:{} \nLoss:{}'.format(scores[1] ,scores[0]))