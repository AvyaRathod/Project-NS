from ctypes.wintypes import SIZE
import tensorflow as tf
import tensorflow.keras as K
import os
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from focal_loss import BinaryFocalLoss
from skimage.io import imread, imshow
from skimage.transform import resize
import matplotlib.pyplot as plt
from unet_models import Attention_ResUNet, Attention_UNet, UNet, dice_coef,dice_coef_loss,jacard_coef,jacard_coef_loss

SIZE = 128
IMG_CHANNELS = 3 #for colour channels in image

#Acessing the photos for training and testing

#train images and masks
TRAIN_PATH = 'UNET/Nuclei/data-science-bowl-2018/stage1_train/'
train_ids = next(os.walk(TRAIN_PATH))[1]

images_dataset = np.zeros((len(train_ids), SIZE,SIZE, IMG_CHANNELS), dtype=np.uint8)
masks_dataset = np.zeros((len(train_ids), SIZE,SIZE, 1), dtype=np.bool_)

print('Resizing training images and masks')
for n, id_ in tqdm(enumerate(train_ids), total = len(train_ids)):
    path =  TRAIN_PATH + id_
    img = imread(path + '/images/' + id_ +'.png')[:,:,:IMG_CHANNELS]
    img = resize(img,(SIZE,SIZE), mode = 'constant', preserve_range=True)    
    images_dataset[n]= img # Fill empty X_TRAIN with values from image
    mask = np.zeros((SIZE, SIZE,1),dtype = np.bool_)
    for mask_file in next(os.walk(path+'/masks/'))[2]:
        mask_ = imread(path + '/masks/'+ mask_file)
        mask_ = np.expand_dims(resize(mask_,(SIZE,SIZE), mode = 'constant',preserve_range =True), axis = -1)
        mask = np.maximum(mask,mask_)
    
    masks_dataset[n] = mask


images_dataset = np.array(images_dataset)/255.
#masks_dataset = np.expand_dims((np.array(masks_dataset)),3)/255.

X_train, X_test, y_train, y_test = train_test_split(images_dataset,masks_dataset,test_size=0.1)

IMG_HEIGHT = X_train.shape[1]
IMG_WIDTH = X_train.shape[2]
IMG_CHANNELS = X_train.shape[3]
loss_func = BinaryFocalLoss(gamma=2)
num_labesls = 1
input_shape = (IMG_HEIGHT,IMG_WIDTH,IMG_CHANNELS)
batch_size = 16
max_epochs= 20

'''
UNET
'''
unet_model = UNet(input_shape)
unet_model.compile(optimizer='adam',loss=loss_func,metrics=['accuracy',jacard_coef])

print(unet_model.summary())

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3,monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='logs'),
]

unet_history = unet_model.fit(X_train,y_train,verbose=1,batch_size = batch_size, validation_data = (X_test,y_test),shuffle=False,epochs=max_epochs,callbacks=callbacks)

unet_model.save('UNET_NEW')
'''

ATTENTION UNET
'''
"""att_unet_model = Attention_UNet(input_shape)
att_unet_model.compile(optimizer='adam',loss=loss_func,metrics=['accuracy',jacard_coef])

print(att_unet_model.summary())

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3,monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='logs'),
]

att_unet_history = att_unet_model.fit(X_train,y_train,verbose=1,batch_size = batch_size, validation_data = (X_test,y_test),shuffle=False,epochs=max_epochs,callbacks=callbacks)

att_unet_model.save('attention_unet.hdf5')"""

'''
ATTENTION RES-UNET
'''
"""att_resunet_model = Attention_ResUNet(input_shape)
att_resunet_model.compile(optimizer='adam',loss=loss_func,metrics=['accuracy',jacard_coef])

print(att_resunet_model.summary())

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3,monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='logs'),
]

att_resunet_history = att_resunet_model.fit(X_train,y_train,verbose=1,batch_size = batch_size, validation_data = (X_test,y_test),shuffle=False,epochs=max_epochs,callbacks=callbacks)

att_resunet_model.save('attention_residual_unet.hdf5')
"""
#########################################################

unet_history_df = pd.DataFrame(unet_history.history)
"""att_unet_history_df = pd.DataFrame(att_unet_history.history)
att_resunet_history_df = pd.DataFrame(att_resunet_history.history)"""

with open('unet_history_df.csv',mode='w') as f:
    unet_history_df.to_csv(f)

history = unet_history
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss)+1)
plt.plot(epochs,loss,'y', label='Training loss')
plt.plot(epochs,val_loss,'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc = history.history['jacard_coef']
val_acc = history.history['val_jacard_coef']

plt.plot(epochs, acc, 'y', label='Training Jacard')
plt.plot(epochs, val_acc, 'r', label='Validation Jacard')
plt.title('Traininf and validation Jacard')
plt.xlabel('Epochs')
plt.ylabel('Jacard')
plt.legend()
plt.show()
"""
with open('att_unet_history_df.csv',mode='w') as f:
    att_unet_history_df.to_csv(f)

history = att_unet_history
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss)+1)
plt.plot(epochs,loss,'y', label='Training loss')
plt.plot(epochs,val_loss,'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc = history.history['jacard_coef']
val_acc = history.history['val_jacard_coef']

plt.plot(epochs, acc, 'y', label='Training Jacard')
plt.plot(epochs, val_acc, 'r', label='Validation Jacard')
plt.title('Traininf and validation Jacard')
plt.xlabel('Epochs')
plt.ylabel('Jacard')
plt.legend()
plt.show()

with open('att_resunet_history_df.csv',mode='w') as f:
    att_resunet_history_df.to_csv(f)

history = att_resunet_history
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss)+1)
plt.plot(epochs,loss,'y', label='Training loss')
plt.plot(epochs,val_loss,'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc = history.history['jacard_coef']
val_acc = history.history['val_jacard_coef']

plt.plot(epochs, acc, 'y', label='Training Jacard')
plt.plot(epochs, val_acc, 'r', label='Validation Jacard')
plt.title('Traininf and validation Jacard')
plt.xlabel('Epochs')
plt.ylabel('Jacard')
plt.legend()
plt.show()
"""

model = unet_model
#model = att_unet_model
#model = att_resunet_model

"""model_path = './unet.hdf5'
model_path = './attention_unet.hdf5'
model_path = './attention_residual_unet.hdf5'
"""
model = tf.keras.models.load_model('UNET_NEW')

test_img_number = random.randint(0, X_test.shape[0]-1)
test_img = X_test[test_img_number]
ground_truth = y_test[test_img_number]

test_img_input = np.expand_dims(test_img,0)
prediction = (model.predict(test_img_input)[0,:,:,0]>0.5).astype(np.uint8)

plt.figure(figsize=(16,8))
plt.subplot(231)
plt.title('Testing image')
plt.imshow(test_img, cmap='gray')
plt.subplot(232)
plt.title('Testing Label')
plt.imshow(ground_truth[:,:,0], cmap='gray')
plt.subplot(233)
plt.title('Prediction on test image')
plt.imshow(prediction, cmap='gray')

plt.show()