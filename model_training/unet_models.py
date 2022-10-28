import tensorflow as tf
import os
import numpy as np
from tensorflow.keras import models, layers, regularizers
from tensorflow.keras import backend as K


# loss coefs

def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2.0 * intersection + 1.0)/(K.sum(y_true_f)+K.sum(y_pred_f) + 1.0)

def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

def jacard_coef(y_true,y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (intersection + 1.0)/(K.sum(y_true_f)+K.sum(y_pred_f) - intersection + 1.0)

def jacard_coef_loss(y_true, y_pred):
    return -jacard_coef(y_true, y_pred)

#building blocks for UNET
def conv_block(x,filter_size,size,dropout, batch_norm=False):
    conv = layers.Conv2D(size, (filter_size,filter_size), padding="same")(x)
    if batch_norm is True:
        conv = layers.BatchNormalization(axis=3)(conv)
    conv = layers.Activation("relu")(conv)

    conv = layers.Conv2D(size, (filter_size,filter_size), padding="same")(conv)
    if batch_norm is True:
        conv = layers.BatchNormalization(axis=3)(conv)
    conv = layers.Activation("relu")(conv)

    if dropout > 0:
        conv = layers.Dropout(dropout)(conv)
    
    return conv

def repeat_elem(tensor, rep):

    return layers.Lambda(lambda x, repnum : K.repeat_elements(x,repnum,axis=3),arguments={'repnum':rep})(tensor)

def res_conv_block(x,filter_size, size, dropout, batch_norm=False):
    '''
    Residual conv layer
    2 options:
        1. activation function before the addition with shortcut
        2. after the addition(which would be as proposed in the original resnet)
    '''
    conv = layers.Conv2D(size, (filter_size,filter_size), padding="same")(x)
    if batch_norm is True:
        conv = layers.BatchNormalization(axis=3)(conv)
    conv = layers.Activation("relu")(conv)
    
    conv = layers.Conv2D(size, (filter_size,filter_size), padding="same")(conv)
    if batch_norm is True:
        conv = layers.BatchNormalization(axis=3)(conv)
    #conv = layers.Activation("relu")(conv)       #Activation before addtion with shortcut

    if dropout > 0:
        conv = layers.Dropout(dropout)(conv)

    shortcut = layers.Conv2D(size,kernel_size = (1,1),padding='same')(x)
    if batch_norm is True:
        shortcut = layers.BatchNormalization(axis=3)(shortcut)
    
    res_path =layers.add([shortcut, conv])
    res_path = layers.Activation('relu')(res_path)    #Activation after addtion with shortcut
    return res_path

def gating_signal(input,out_size,batch_norm=False):
    x = layers.Conv2D(out_size,(1,1), padding='same')(input)
    if batch_norm is True:
        x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    return x

def attention_block(x,gating,inter_shape):
    shape_x = K.int_shape(x)
    shape_g = K.int_shape(gating)

    #Getting x to the same shape as the gating signal
    theta_x = layers.Conv2D(inter_shape,(2,2),strides=(2,2),padding='same')(x)
    shape_theta_x = K.int_shape(theta_x)

    #getting the gating signal to the same number of filters as the inter_shape
    phi_g = layers.Conv2D(inter_shape,(1,1),padding='same')(gating)
    upsample_g = layers.Conv2DTranspose(inter_shape,(3,3),strides=(shape_theta_x[1] // shape_g[1],shape_theta_x[2]//shape_g[2]), padding='same')(phi_g)

    concat_xg = layers.add([upsample_g,theta_x])
    act_xg = layers.Activation('relu')(concat_xg)
    psi = layers.Conv2D(1,(1,1),padding='same')(act_xg)
    sigmoid_xg = layers.Activation('sigmoid')(psi)
    shape_sigmoid = K.int_shape(sigmoid_xg)
    upsample_psi = layers.UpSampling2D(size=(shape_x[1] // shape_sigmoid[1],shape_x[2]//shape_sigmoid[2]))(sigmoid_xg)

    upsample_psi = repeat_elem(upsample_psi,shape_x[3])


    y = layers.multiply([upsample_psi,x])

    result = layers.Conv2D(shape_x[3],(1,1),padding='same')(y)
    result_bn = layers.BatchNormalization()(result)
    return result_bn

def UNet(input_shape, NUM_CLASSES = 1, dropout_rate=0.1, batch_norm=True):
    #network structure
    FILTER_NUM = 64
    FILTER_SIZE = 3
    UP_SAMP_SIZE = 2

    inputs = layers.Input(input_shape, dtype=tf.float32)

    #Downsampling layers
    #DownRes 1, convolution +pooling
    conv_128 = conv_block(inputs, FILTER_SIZE, FILTER_NUM, dropout_rate,batch_norm)
    pool_64 = layers.MaxPooling2D(pool_size=(2,2))(conv_128)
    #DownRes 2
    conv_64 = conv_block(pool_64, FILTER_SIZE, 2*FILTER_NUM, dropout_rate,batch_norm)
    pool_32 = layers.MaxPooling2D(pool_size=(2,2))(conv_64)
    #DownRes 3
    conv_32 = conv_block(pool_32, FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)
    pool_16 = layers.MaxPooling2D(pool_size=(2,2))(conv_32)
    #DownRes 4
    conv_16 = conv_block(pool_16, FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)
    pool_8 = layers.MaxPooling2D(pool_size=(2,2))(conv_16)
    #DownRes 5
    conv_8 = conv_block(pool_8, FILTER_SIZE, 16*FILTER_NUM, dropout_rate, batch_norm)

    #Upsampling Layers
    #UpRes 6
    up_16 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(conv_8)
    up_16 = layers.concatenate([up_16,conv_16], axis=3)
    up_conv_16 = conv_block(up_16,FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 7
    up_32 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_16)
    up_32 = layers.concatenate([up_32,conv_32], axis=3)
    up_conv_32 = conv_block(up_32,FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 8
    up_64 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_32)
    up_64 = layers.concatenate([up_64,conv_64], axis=3)
    up_conv_64 = conv_block(up_64,FILTER_SIZE, 2*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 9
    up_128 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_64)
    up_128 = layers.concatenate([up_128,conv_128], axis=3)
    up_conv_128 = conv_block(up_128,FILTER_SIZE, FILTER_NUM, dropout_rate, batch_norm)

    #1*1 convolutional layers
    conv_final= layers.Conv2D(NUM_CLASSES,kernel_size=(1,1))(up_conv_128)
    conv_final = layers.BatchNormalization(axis=3)(conv_final)
    conv_final = layers.Activation('sigmoid')(conv_final) #change to softmax for multichannel

    #model
    model = models.Model(inputs, conv_final, name="UNet")
    print(model.summary())
    return model


def Attention_UNet(input_shape, NUM_CLASSES = 1, dropout_rate=0.1, batch_norm=True):
    #network structure
    FILTER_NUM = 64
    FILTER_SIZE = 3
    UP_SAMP_SIZE = 2

    inputs = layers.Input(input_shape, dtype=tf.float32)

    #Downsampling layers
    #DownRes 1, convolution +pooling
    conv_128 = conv_block(inputs, FILTER_SIZE, FILTER_NUM, dropout_rate,batch_norm)
    pool_64 = layers.MaxPooling2D(pool_size=(2,2))(conv_128)
    #DownRes 2
    conv_64 = conv_block(pool_64, FILTER_SIZE, 2*FILTER_NUM, dropout_rate,batch_norm)
    pool_32 = layers.MaxPooling2D(pool_size=(2,2))(conv_64)
    #DownRes 3
    conv_32 = conv_block(pool_32, FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)
    pool_16 = layers.MaxPooling2D(pool_size=(2,2))(conv_32)
    #DownRes 4
    conv_16 = conv_block(pool_16, FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)
    pool_8 = layers.MaxPooling2D(pool_size=(2,2))(conv_16)
    #DownRes 5
    conv_8 = conv_block(pool_8, FILTER_SIZE, 16*FILTER_NUM, dropout_rate, batch_norm)

    #Upsampling Layers
    #UpRes 6
    gating_16 = gating_signal(conv_8,8*FILTER_NUM, batch_norm)
    att_16 = attention_block(conv_16, gating_16, 8*FILTER_NUM)
    up_16 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(conv_8)
    up_16 = layers.concatenate([up_16,att_16], axis=3)
    up_conv_16 = conv_block(up_16,FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 7
    gating_32 = gating_signal(up_conv_16,4*FILTER_NUM, batch_norm)
    att_32 = attention_block(conv_32, gating_32, 4*FILTER_NUM)
    up_32 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_16)
    up_32 = layers.concatenate([up_32,att_32], axis=3)
    up_conv_32 = conv_block(up_32,FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 8
    gating_64 = gating_signal(up_conv_32,2*FILTER_NUM, batch_norm)
    att_64 = attention_block(conv_64, gating_64, 2*FILTER_NUM)
    up_64 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_32)
    up_64 = layers.concatenate([up_64,att_64], axis=3)
    up_conv_64 = conv_block(up_64,FILTER_SIZE, 2*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 9
    gating_128 = gating_signal(up_conv_64,FILTER_NUM, batch_norm)
    att_128 = attention_block(conv_128, gating_128, FILTER_NUM)
    up_128 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_64)
    up_128 = layers.concatenate([up_128,att_128], axis=3)
    up_conv_128 = conv_block(up_128,FILTER_SIZE, FILTER_NUM, dropout_rate, batch_norm)

    #1*1 convolutional layers
    conv_final= layers.Conv2D(NUM_CLASSES,kernel_size=(1,1))(up_conv_128)
    conv_final = layers.BatchNormalization(axis=3)(conv_final)
    conv_final = layers.Activation('sigmoid')(conv_final) #change to softmax for multichannel

    #model
    model = models.Model(inputs, conv_final, name="Attention_UNet")
    print(model.summary())
    return model

def Attention_ResUNet(input_shape, NUM_CLASSES = 1, dropout_rate=0.1, batch_norm=True):
    #network structure
    FILTER_NUM = 64
    FILTER_SIZE = 3
    UP_SAMP_SIZE = 2

    inputs = layers.Input(input_shape, dtype=tf.float32)

    #Downsampling layers
    #DownRes 1, convolution +pooling
    conv_128 = res_conv_block(inputs, FILTER_SIZE, FILTER_NUM, dropout_rate,batch_norm)
    pool_64 = layers.MaxPooling2D(pool_size=(2,2))(conv_128)
    #DownRes 2
    conv_64 = res_conv_block(pool_64, FILTER_SIZE, 2*FILTER_NUM, dropout_rate,batch_norm)
    pool_32 = layers.MaxPooling2D(pool_size=(2,2))(conv_64)
    #DownRes 3
    conv_32 = res_conv_block(pool_32, FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)
    pool_16 = layers.MaxPooling2D(pool_size=(2,2))(conv_32)
    #DownRes 4
    conv_16 = res_conv_block(pool_16, FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)
    pool_8 = layers.MaxPooling2D(pool_size=(2,2))(conv_16)
    #DownRes 5
    conv_8 = res_conv_block(pool_8, FILTER_SIZE, 16*FILTER_NUM, dropout_rate, batch_norm)

    #Upsampling Layers
    #UpRes 6
    gating_16 = gating_signal(conv_8,8*FILTER_NUM, batch_norm)
    att_16 = attention_block(conv_16, gating_16, 8*FILTER_NUM)
    up_16 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(conv_8)
    up_16 = layers.concatenate([up_16,att_16], axis=3)
    up_conv_16 = res_conv_block(up_16,FILTER_SIZE, 8*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 7
    gating_32 = gating_signal(up_conv_16,4*FILTER_NUM, batch_norm)
    att_32 = attention_block(conv_32, gating_32, 4*FILTER_NUM)
    up_32 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_16)
    up_32 = layers.concatenate([up_32,att_32], axis=3)
    up_conv_32 = res_conv_block(up_32,FILTER_SIZE, 4*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 8
    gating_64 = gating_signal(up_conv_32,2*FILTER_NUM, batch_norm)
    att_64 = attention_block(conv_64, gating_64, 2*FILTER_NUM)
    up_64 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_32)
    up_64 = layers.concatenate([up_64,att_64], axis=3)
    up_conv_64 = res_conv_block(up_64,FILTER_SIZE, 2*FILTER_NUM, dropout_rate, batch_norm)

    #UpRes 9
    gating_128 = gating_signal(up_conv_64,FILTER_NUM, batch_norm)
    att_128 = attention_block(conv_128, gating_128, FILTER_NUM)
    up_128 = layers.UpSampling2D(size=(UP_SAMP_SIZE,UP_SAMP_SIZE), data_format='channels_last')(up_conv_64)
    up_128 = layers.concatenate([up_128,att_128], axis=3)
    up_conv_128 = res_conv_block(up_128,FILTER_SIZE, FILTER_NUM, dropout_rate, batch_norm)

    #1*1 convolutional layers
    conv_final= layers.Conv2D(NUM_CLASSES,kernel_size=(1,1))(up_conv_128)
    conv_final = layers.BatchNormalization(axis=3)(conv_final)
    conv_final = layers.Activation('sigmoid')(conv_final) #change to softmax for multichannel

    #model
    model = models.Model(inputs, conv_final, name="Attention_UNet")
    print(model.summary())
    return model