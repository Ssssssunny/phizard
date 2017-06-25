import numpy as np
from numpy import pi

EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

def one_loop():
    def sin_cos(a, b):
        t = np.array([0, 1, 2, 3, 4, 5, 6])
        c = a*np.sin((2*pi*t)/7)+b*np.cos(2*pi*t/7)
        return c
    origin_data = []
    for ii in range(8):
        a = np.random.rand()
        b = np.random.rand()
        origin_data.append(sin_cos(a, b))
    origin_data = np.array(origin_data)
    b = np.exp(origin_data)
    sum = np.sum(b, axis=0, keepdims=True)
    softmax = b/sum
    return softmax

def generator(number_of_iteration, loop_step):
    data = []
    one_week = one_loop()
    for ii in range(number_of_iteration):
        data.append(one_week)

    data = np.array(data)
    data = np.concatenate(data, axis=-1)
    shape = data.shape
    noise = np.random.randn(shape[0], shape[1])*0.01
    data = noise + data
    b = np.exp(data)
    sum = np.sum(b, axis=0, keepdims=True)
    softmax = b/sum
    return softmax



if __name__=='__main__':

    data = generator(5, 7)
    # print ('test:', np.sum(data, axis=0))
    # print ('test:', data.shape)
    # plt.plot(data[1])
    # plt.show()
