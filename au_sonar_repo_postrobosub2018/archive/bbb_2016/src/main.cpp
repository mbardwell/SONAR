#include <stdlib.h>
#include <csignal>
#include <iostream>
#include <algorithm>
#include <cmath>

#include <alglib/src/fasttransforms.h>
#include <au_sonar/sample.h>

using namespace std;
using namespace au_sonar;

const std::string out_file = "~/arvp/lags.csv";

void print_vec(double* v, int n)
{
    ofstream stream;
    stream.open( out_file.c_str() );

    cout << "Streaming to file " << out_file << "... ";

    for(int i = 0; i < n; i++)
    {
        stream << v[i] << "," << endl;
        //cout << v[i] << endl;
    }

    cout << "complete." << endl;

    stream.close();
}

double get_phase_shift(double normalized, bool up)
{
    double angle = acos(normalized);

    if(up) {
        return angle;
    }
    else {
        // reflect
        return 2 * PI - angle;
    }
}

void interruptHandler( int signum ) {
   cout << "Interrupt signal (" << signum << ") received.\n";

   // terminate program
   exit(signum);
}

int main(int argc, char** argv) {
   signal(SIGINT, interruptHandler);

   //int array[15] = { 1, 5, 2, 3, 6, 6, 8, 10, 4, 8, 3, 1, 1, 6, 7 };

   //int* max = max_element(array, array + 15);
   //ptrdiff_t m_offset = max - array;
   //cout << "MAX: " << *max << " OFFSET: " << m_offset << " " << array[m_offset] << endl;

   vector<double> h1_samples, h2_samples;
   double amplitude = 0;

   if( test_sample(h1_samples, h2_samples, amplitude) )
   {
       alglib::real_1d_array h1, h2, r;

       h1.setcontent(h1_samples.size(), &(h1_samples[0]));
       h2.setcontent(h2_samples.size(), &(h2_samples[0]));

       // Cross-correlation
       alglib::corrr1d(h1, h1_samples.size(), h2, h2_samples.size(), r);

       double* first_lag = r.getcontent();
       double* last_lag = first_lag + h1_samples.size() - 1; // + h2_samples.size() - 2;

       double* max_lag = max_element(first_lag, first_lag + 20/*last_lag*/);
       double* min_lag = min_element(first_lag, first_lag + 20);

       ptrdiff_t offset = max_lag - first_lag;

       double normalized = 2 * (*first_lag - *min_lag) / (*max_lag - *min_lag) - 1; // normalizes the value to between -1 and 1
       double phase_shift = get_phase_shift(normalized, *first_lag < *(first_lag + 1));
       //double phase_shift = fmod(2 * PI * offset * SONAR_TEST_FREQ / SAMPLE_FREQ, 2*PI);

       printf("First Lag: %lf.0 Max Lag: %lf.0 Offset: %ld Amplitude: %lf.2 Phase Shift: %lf.2\n", *first_lag, *max_lag, offset, amplitude, phase_shift * RADIANS_TO_DEGREES);

       print_vec(r.getcontent(), 12500);
   }

   return 0;
}

//for angle [0, 45 ...]
    // Turn Servo to desired angle (blocking call)
    //
    // Sample 12500 voltage readings from hydrophones (50ms)
    // Get Amplitude

    // while (amplitude is bad)
        // Sample 12500 voltage readings from hydrophones (50ms)
        // Get Amplitude
        // if (amplitude is good) break;
        // else set potentiometer

    // Cross correlation on hydrophone 1 and 2 -- returns lag time
    // store in lag array

// servo_heading = What angle returned max lag (curve analysis)

// struct OutputToJetson output;
// output.relative_heading = servo_heading + offset;
// output.amplitude = one of the amplitudes (all the same) / gain;
