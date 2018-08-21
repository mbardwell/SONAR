#!/usr/bin/python

from __future__ import print_function
import sys
import os
import csv
import numpy as np

def usage():
    print('Usage: dat2csv.py input_file.dat [output_file.csv]')
    print('Usage: dat2csv.py input_directory [output_directory]')
    exit(1)

'''
converts a dat file to a csv file
param:
    * input_file - dat file name
    * output_file - csv file name
return: samples written
'''
def conv2csv(input_file, output_file):
    data = None
    with open(input_file, 'rb') as dat_file:
        data = dat_file.read()
        data = np.fromstring(data, dtype=np.uint16)

    with open(output_file, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # iterate over n/2 samples
        for row in range(1, len(data)/2-1):
            csv_writer.writerow([data[row*2], data[row*2+1]])

    return len(data)/2-1;

if __name__ == '__main__':
    # read arguments
    input_name = None
    output_name = None
    if len(sys.argv) >= 2:
        input_name = sys.argv[1]
        if len(sys.argv) >= 3:
            output_name = sys.argv[2]
    else:
        usage()

    # check if reading one file or batch
    if (os.path.isfile(input_name)):
        if output_name == None:
            # create an output file name
            output_name, _ = os.path.splitext(input_name)
            output_name += '.csv'
        print('processing file:' + input_name)
        n = conv2csv(input_name, output_name)
        print('\t' + str(n) + ' samples written')
    elif (os.path.isdir(input_name)):
        # if output dir does not exist create it
        if output_name and not os.path.exists(output_name):
            os.makedirs(output_name)
        # get list of files
        input_files = [f for f in os.listdir(input_name)
                        if os.path.isfile(os.path.join(input_name, f)) and f.endswith(".dat")]
        # process each file
        for f in input_files:
            # create an output file name
            output_file, _ = os.path.splitext(f)
            output_file += '.csv'
            if output_name != None:
                output_file = os.path.join(output_name, output_file)
            else:
                output_file = os.path.join(input_name, output_file)
            print('processing file:' + f)
            n = conv2csv(os.path.join(input_name, f), output_file)
            print('\t' + str(n) + ' samples written')
    else:
        print('File/directory specified does not exist')
        exit(1)
