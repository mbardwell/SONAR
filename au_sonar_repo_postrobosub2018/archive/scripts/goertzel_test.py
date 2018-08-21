#!/usr/bin/env python

from types import *
import matplotlib.pyplot as plt
import numpy as np

class Goertzel:
    def __init__( self, target_freq, block_size, sample_rate ):
        self.block_size = block_size
        self.bin_num = int( 0.5 + ( block_size * target_freq ) / float( sample_rate ) )
        self.omega = ( 2 * np.pi / block_size ) * self.bin_num
        self.cosine = np.cos( self.omega )
        self.sine = np.sin( self.omega )
        self.coeff = 2 * self.cosine

        self.reset()

    def reset( self ):
        self.q0 = self.q1 = self.q2 = 0.0
        self.real = self.imaginary = 0.0

    def calculate( self, samples ):
        if len( samples ) != self.block_size:
            raise ValueError( 'samples does not have the same length as initialized block size' )

        for sample in samples:
            self.q2 = self.q1
            self.q1 = self.q0
            self.q0 = self.coeff * self.q1 - self.q2 + sample

        self.real = self.q1 - self.q2 * self.cosine
        self.imaginary = self.q2 * self.sine

    def get_magnitude( self ):
        return np.math.sqrt( np.power( self.real, 2 ) + np.power( self.imaginary, 2 ) )

    def get_phase( self ):
        return np.arctan2( self.imaginary, self.real )

def goertzel_test( target_freq, block_size, sample_rate ):
    x_range = np.arange( block_size )
    noise = 0.1 * np.random.normal( 0, 1, block_size )
    signal = ( [ np.sin( 2 * np.pi * target_freq * ( i / float( sample_rate ) ) ) for i in x_range ] + noise ) * np.hanning( block_size )
    delayed_signal = ( [ np.sin( 2 * np.pi * target_freq * ( i / float( sample_rate ) ) + ( np.pi / 4 ) ) for i in x_range ] + noise ) * np.hanning( block_size )

    goertzel = Goertzel( target_freq, block_size, sample_rate )
    goertzel.calculate( signal )
    phase = goertzel.get_phase()
    goertzel.reset()

    goertzel.calculate( delayed_signal )
    delayed_phase = goertzel.get_phase()

    print 'Calculated phase difference %r' % np.degrees( phase - delayed_phase )

if __name__ == '__main__':
    goertzel_test( 30000, 150, 400000 )
