import os

import matplotlib.pyplot as plt
import numpy as np


def list_data(folder='data'):
    return [f for f in os.listdir(folder) if f.find('.log.') > -1]


def reject_outliers(input_arr, m=2):
    return input_arr[abs(input_arr - np.mean(input_arr)) < m * np.std(input_arr)]


def clean_data(filename):
    data_lines = open('data/{}'.format(filename)).readlines()
    arr = []
    digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    for l in data_lines:
        arr += [float(x) for x in l.split(',') if len(x) > 0 and x[0] in digits]
    arr = reject_outliers(np.asarray(arr))
    window = 11
    weight = np.ones(window) / float(window)
    out = np.convolve(arr, weight / weight.sum(), 'same')
    output_file = open('clean-data/{}'.format(filename), 'w')
    output_file.write(','.join([str(x) for x in out]))
    output_file.close()


def plot_data(filename):
    arr = [float(x) for x in open('clean-data/{}'.format(filename)).readline().split(',')]
    x = np.arange(len(arr))
    plt.plot(x, arr)
    fig = plt.gcf()
    fig.set_size_inches(30, 10)
    fig.savefig('plot/{}.png'.format(filename))
    plt.clf()


for f in list_data('data'):
    clean_data(f)

for f in list_data('clean-data'):
    plot_data(f)
