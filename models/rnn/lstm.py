import numpy as np
from numpy import arange, sin, pi, random
#import matplotlib.pyplot as plt


from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import load_model

from phizard.models.statistics import grubbs_test
STEP_LENGTH = 50

def initial():
    t = np.arange(0.0, 10.0, 0.01)
    wave1 = sin(2*2*pi*t)
    noise = random.normal(0, 0.1, len(t))
    wave1 = wave1 + noise
    wave2 = sin(2 * pi * t)
    t_rider = arange(0.0, 0.5, 0.01)
    wave3 = sin(10 * pi * t_rider)
    insert = round(0.8 * len(t))
    wave1[int(insert):int(insert) + 50] = wave1[int(insert):int(insert) + 50] + wave3
    return wave1 + wave2

def test_wave():
    t = np.arange(0.0, 10.0, 0.01)
    wave1 = sin(1.5 * 1.5 * pi * t)
    noise = random.normal(0, 0.1, len(t))
    wave1 = wave1 + noise
    wave2 = sin(1.5 * pi * t)
    t_rider = arange(0.0, 0.5, 0.01)
    wave3 = sin(10 * pi * t_rider)
    insert = round(0.8 * len(t))
    wave1[int(insert):int(insert) + 50] = wave1[int(insert):int(insert) + 50] + wave3
    return wave1+wave2

def Phizard_model(sequence_length):
    model = Sequential()
    layers = {'input': 1, 'hidden1': 64, 'hidden2': 256, 'hidden3': 100, 'output': 1}
    model.add(LSTM(input_length=sequence_length - 1, input_dim=layers['input'],
            output_dim=layers['hidden1'],
            return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(layers['hidden2'], return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(layers['hidden3'], return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(output_dim=layers['output']))
    model.add(Activation("linear"))
    model.compile(loss="mse", optimizer="rmsprop")
    return model

def split_data(data, sequence_length):
    """
    :param data: 1-D np.array
    :return:
    """
    train_data = []
    train_labels = []
    for ii in range(len(data)-sequence_length):
        train_data.append(data[ii:ii+sequence_length-1])
        train_labels.append(data[ii+sequence_length-1])
    return np.array(train_data), np.array(train_labels)

def train_model(data, save_path):
    sequence_length = STEP_LENGTH
    train_data, train_labels = split_data(data, sequence_length)
    test_data, test_labels = split_data(data, sequence_length)
    shape = train_data.shape
    train_data = np.reshape(train_data, [shape[0], shape[1], 1])
    test_data = np.reshape(test_data, [shape[0], shape[1], 1])
    model = Phizard_model(sequence_length)
    model.fit(train_data, train_labels, batch_size=100, nb_epoch=20)
    test_predict = model.predict(test_data)
    print ('test predict:', test_predict, test_predict.shape)
    print ('test labels;', test_labels, test_labels.shape)
    # plt.figure(1)
    # plt.subplot(311)
    # plt.title("test predict")
    # plt.plot(test_predict, 'b')
    # plt.subplot(312)
    # plt.title("original Signal")
    # plt.plot(test_labels, 'g')
    # plt.subplot(313)
    # plt.title("error")
    # plt.plot(test_labels-np.squeeze(test_predict), 'g')
    # plt.show()
    return test_labels-np.squeeze(test_predict)



def load_model_predict(file_path):
    sequence_length = STEP_LENGTH
    model = load_model(file_path)
    # model.save('/home/liyuanpeng/Desktop/day3/Teemo/yuanpeng/yuanpeng_dtnn_model/my_model.h5')
    # model = load_model('/home/liyuanpeng/Desktop/day3/Teemo/yuanpeng/yuanpeng_dtnn_model/my_model.h5')
    test_diff = test_wave()
    diff_wave, diff_labels = split_data(test_diff[500:], sequence_length)
    shape = diff_wave.shape
    diff_wave = np.reshape(diff_wave, [shape[0], shape[1], 1])
    diff_predict = model.predict(diff_wave)
    # plt.figure(2)
    # plt.subplot(311)
    # plt.title("diff predict")
    # plt.plot(diff_predict, 'b')
    # plt.subplot(312)
    # plt.title("origin wave")
    # plt.plot(diff_labels, 'g')
    # plt.subplot(313)
    # plt.title("error")
    # plt.plot(diff_labels-np.squeeze(diff_predict), 'g')
    # plt.show()
    return diff_labels-np.squeeze(diff_predict)

def get_result(series, save_path='../my_model.h5'):
    residue = train_model(series, save_path)
    return residue

if __name__=="__main__":
    data = initial()
    residue = get_result(data)
    outlines = grubbs_test(residue)

