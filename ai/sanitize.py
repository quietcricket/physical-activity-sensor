import os

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


def list_data(folder='data'):
    return [f for f in os.listdir(folder) if f.endswith('txt')]


def replace_outliers(input_arr, m=1.5):
    mean=np.mean(input_arr)
    threshold=np.std(input_arr)*m
    arr=[0]*len(input_arr)
    for i in range(0,len(input_arr)):
        if abs(input_arr[i]-mean)>threshold:
            arr[i]=mean
        else:
            arr[i]=input_arr[i]
    return arr


def clean_data(filename):
    data_lines = open('data/{}'.format(filename)).readlines()
    output_file = open('clean-data/{}'.format(filename), 'w')
    t=datetime.strptime('00:01','%H:%M')
    empty_record=','.join(['']*600)

    window = 11
    weight = np.ones(window) / float(window)

    all_data=[None]*60*24
    max_index=0
    for l in data_lines:
        # Avoid empty lines
        if len(l)<3:
            continue
        arr = l.split(',')
        hh,mm=arr[0].split(':')
        index=int(hh)*60+int(mm)

        while all_data[index] is not None:
            index+=1

        arr=replace_outliers([float(x) for x in arr[1:]])
        # Gives more problem than solving it, not using it now.
        # Replace outliers give better result
        # out = np.convolve(np.asarray(arr), weight / weight.sum(), 'same')
        all_data[index]=','.join(str(x) for x in arr)
        max_index=index
    for i in range(0,len(all_data)):
        if all_data[i] is None:
            if i>1 and i<max_index:
                all_data[i]=all_data[i-1]
            else:
                all_data[i]=empty_record
    output_file.write(",".join(all_data))
    output_file.close()


def plot_data(filename):
    arr = [0 if x=='' else float(x) for x in open('clean-data/{}'.format(filename)).readline().split(',')]
    
    x = np.arange(len(arr))
    plt.plot(x, arr)
    fig = plt.gcf()
    fig.set_size_inches(30, 10)
    fig.savefig('plot/{}.png'.format(filename[:-4]))
    plt.clf()


for f in list_data('data'):
    clean_data(f)

for f in list_data('clean-data'):
    plot_data(f)
