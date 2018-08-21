#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt
import numpy as np

class CSVReader:
	def __init__( self, directory, csv_file ):
		self.directory = directory
		self.csv_file = csv_file

	def unpack( self ):		
		time = []
		volts_1 = []
		volts_2 = []

		with open( self.directory + self.csv_file, 'rb' ) as csv_file:
			data_reader = csv.reader( csv_file, delimiter=',' )
			title = data_reader.next()
			units = data_reader.next()
			for row in data_reader:
				time.append( np.float32(row[0]) )
				volts_1.append( np.float32(row[1]) )
				volts_2.append( np.float32(row[2]) )
		
		return title, units, time, volts_1, volts_2

	def change_file( self, directory, csv_file ):
		if( directory != None ):
			self.directory = directory
		if( csv_file != None ):
			self.csv_file = csv_file

class Goertzel:
    def __init__( self, target_freq, block_size, sample_rate ):
        self.block_size = np.uint32( block_size )
        self.bin_num = np.uint32( 0.5 + ( block_size * target_freq ) / np.float32( sample_rate ) )
        self.omega = ( 2 * np.pi / self.block_size ) * self.bin_num
        self.cosine = np.cos( self.omega )
        self.sine = np.sin( self.omega )
        self.coeff = 2 * self.cosine

        self.reset()

    def reset( self ):
        self.q0 = self.q1 = self.q2 = np.float32( 0.0 )
        self.real = self.imaginary = np.float32( 0.0 )

    def calculate( self, samples ):
        if len( samples ) != self.block_size:
            raise ValueError( 'samples does not have the same length as initialized block size' )

        for sample in samples:
            self.q2 = self.q1
            self.q1 = self.q0
            self.q0 = self.coeff * self.q1 - self.q2 + np.float32( sample )

        self.real = self.q1 - self.q2 * self.cosine
        self.imaginary = self.q2 * self.sine

    def get_magnitude( self ):
        return np.math.sqrt( np.power( self.real, 2 ) + np.power( self.imaginary, 2 ) )

    def get_phase( self ):
        return np.arctan2( self.imaginary, self.real )

if __name__ == '__main__':
	directory = '/Users/jesset/Downloads/June10th/'
	csv_file = '0m_1.52m_parallel_1.csv'

	target_freq = 27000
	block_size = 128
	sample_rate = 500000

	reader = CSVReader( directory, csv_file )
	goertzel_1 = Goertzel( target_freq, block_size, sample_rate )
	goertzel_2 = Goertzel( target_freq, block_size, sample_rate )

	title, units, time, volts_1, volts_2 = reader.unpack()
	num_windows = ( len( volts_1 ) / block_size ) * block_size
	for i in xrange( 0, num_windows, block_size ):
		goertzel_1.calculate( volts_1[i:i+block_size] * np.hanning( block_size ) )
		goertzel_2.calculate( volts_2[i:i+block_size] * np.hanning( block_size ) )
		print goertzel_1.get_phase() - goertzel_2.get_phase()
		goertzel_1.reset()
		goertzel_2.reset()

	plt.plot( time, volts_1, 'r', label=title[1] )
	plt.plot( time, volts_2, 'b', label=title[2] )
	plt.title( csv_file )

	plt.legend()
	plt.show()
