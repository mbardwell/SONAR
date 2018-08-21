#ifndef __AU_SONAR_SAMPLE_H__
#define __AU_SONAR_SAMPLE_H__

#include <ctime>
#include <cmath>
#include <stdint.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

#define PI 3.14159265
#define DEGREES_TO_RADIANS PI / 180
#define RADIANS_TO_DEGREES 180 / PI

#define SAMPLE_PROFILE
#define SAMPLE_FREQ 250000

#define SONAR_TEST_PHASE_SHIFT 220 * DEGREES_TO_RADIANS
#define SONAR_TEST_FREQ 27000
#define SONAR_TEST_AMP 512 // in mV
#define NOISE_FREQ 10000
#define NOISE_AMP 15 // in mV
#define BASELINE 512

typedef unsigned char byte;

namespace au_sonar
{

template<typename T>
inline T to_sonar_value(byte lsb, byte msb);

template<typename T>
inline T get_amplitude(const std::vector<T>& buffer);

// TODO: Get 3ms on each side of max
template<typename T>
std::vector<T> filter(const std::vector<T>& buffer, size_t pulse_time = 3);

template<typename T>
bool sample_sonar(std::vector<T>& buffer_1, std::vector<T>& buffer_2, T& amplitude, size_t sample_time = 2048);

// TODO: Simulate impulse
template<typename T>
bool test_sample(std::vector<T>& buffer_1, std::vector<T>& buffer_2, T& amplitude, size_t sample_time = 2048);

} // end namespace au_sonar

#endif
