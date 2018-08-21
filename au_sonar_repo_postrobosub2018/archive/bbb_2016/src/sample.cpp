#include <au_sonar/sample.h>

using namespace std;

namespace au_sonar
{

template<typename T>
inline T to_sonar_value(byte lsb, byte msb)
{
    int32_t v = 0;
    v = (v << 8) + msb;
    v = (v << 8) + lsb;
    return static_cast<T>(v);
}

template<typename T>
inline T get_amplitude(const vector<T>& buffer)
{
    return *max_element(buffer.begin(), buffer.end());
}

template<typename T>
void filter(const vector<T>& buffer, T* start_slice, T* end_slice, size_t pulse_time)
{
    size_t pulse_length = pulse_time * SAMPLE_FREQ / 1000;

    double* max_loc = max_element(buffer.begin(), buffer.end());

    ptrdiff_t half_length = pulse_length / 2;
    if (max_loc - buffer.begin() > half_length)
        start_slice = max_loc - half_length;
    else
        start_slice = buffer.begin();

    if (buffer.end() - max_loc > half_length)
        end_slice = max_loc + half_length;
    else
        end_slice = buffer.end();
}

template<typename T>
bool sample_sonar(vector<T>& buffer_1, vector<T>& buffer_2, T& amplitude, size_t sample_time)
{
    ifstream sonar_stream;

    size_t sample_count = sample_time * SAMPLE_FREQ / 1000;
    buffer_1 = vector<T>(sample_count);
    buffer_2 = vector<T>(sample_count);

#ifdef SAMPLE_PROFILE
    time_t start = std::time(0);
#endif

    sonar_stream.open( "/dev/beaglelogic", std::ifstream::in );

#ifdef SAMPLE_PROFILE
    cout << (start - std::time(0)) << " seconds to open" << endl;
#endif

    cout << "Sampling...";

    for(size_t i = 0; i < sample_count; i++)
    {
        byte lsb1, msb1, lsb2, msb2;

        if(sonar_stream.good()) {
            sonar_stream >> lsb1 >> msb1 >> lsb2 >> msb2;

            T v1 = to_sonar_value<T>(lsb1, msb1);
            T v2 = to_sonar_value<T>(lsb2, msb2);

            buffer_1[i] = v1;
            buffer_2[i] = v2;
        }
        else {
            sonar_stream.close();
            return false;
        }

#ifdef SAMPLE_PROFILE
        if((i + 1) % (sample_count / 10) == 0) {
            cout << buffer_1[i] << " " << buffer_2[i] << " " << endl;
            time_t current = std::time(0);
            printf("At %d reads after %d seconds.\n", (int) (i + 1), (int) (current - start));
        }
#endif
    }

    cout << " complete." << endl;

    T amplitude_1 = get_amplitude(buffer_1);
    T amplitude_2 = get_amplitude(buffer_2);

    amplitude = max(amplitude_1, amplitude_2);

    sonar_stream.close();

    return true;
}

template<typename T>
bool test_sample(vector<T>& buffer_1, vector<T>& buffer_2, T& amplitude, size_t sample_time)
{
    size_t sample_count = sample_time * SAMPLE_FREQ / 1000;
    buffer_1 = vector<T>(sample_count);
    buffer_2 = vector<T>(sample_count);

    float sonar_step = SONAR_TEST_FREQ * 2 * PI / (float) sample_count;
    float noise_step = NOISE_FREQ * 2 * PI / (float) sample_count;

    for (size_t i = 0; i < sample_count; i++)
    {
        T sonar_component_1 = SONAR_TEST_AMP * sin(sonar_step * i) + BASELINE;
        T sonar_component_2 = SONAR_TEST_AMP * sin(sonar_step * i + SONAR_TEST_PHASE_SHIFT) + BASELINE;
        T noise_component = NOISE_AMP * sin(noise_step * i);

        buffer_1[i] = sonar_component_1 + noise_component;
        buffer_2[i] = sonar_component_2 + noise_component;

#ifdef SAMPLE_PROFILE
        cout << buffer_1[i] << " " << buffer_2[i] << " ";
#endif
    }

    cout << endl;

    T amplitude_1 = get_amplitude(buffer_1);
    T amplitude_2 = get_amplitude(buffer_2);

    amplitude = max(amplitude_1, amplitude_2);

    return true;
}

template bool sample_sonar<double>(vector<double>&, vector<double>&, double&, size_t);
template bool test_sample<double>(vector<double>&, vector<double>&, double&, size_t);

} //end namespace au_sonar
