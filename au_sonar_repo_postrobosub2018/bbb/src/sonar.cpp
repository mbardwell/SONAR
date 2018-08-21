#include <iostream>
#include <string>
#include <stdexcept>
#include <stdlib.h>
#include <unistd.h>
#include <fstream>

#include "prudaq.h"

sonar::Prudaq* daq;

int main(int argc, char* argv)
{
	// Make sure we're root (needed for PRU)
	if (geteuid() != 0) {
		std::cout << "Must be root.  Try again with sudo." << std::endl;
		return EXIT_FAILURE;
	}

	// initialize the PRUDaq object
	try
	{
		daq = new sonar::Prudaq(500000, "firmware/pru0.bin", "firmware/pru1.bin");
	}
	catch(const std::runtime_error& e)
	{
		std::cout << e.what() << std::endl;
		return EXIT_FAILURE;
	}

	uint32_t* data = NULL;
	while(1)
	{
		// get values from DAQ
		uint32_t bytes_read = daq->getData(data);
		data = daq->local_buf;

		usleep(100);
	}
	return 0;
}

// if read data publish it
//		for(int i=0; i<bytes_read; i++)
//		{
//			sonar::SonarRaw raw_x;
//
//			// raw_x.header.stamp = ros::Time::now();
//
//			// each 32-bit word holds a pair of samples (one from each channel)
//			// samples are 10bits
//			// remaining bytes records the clock and the input select state
//			raw_x.ref = (data[i] & 0x03FF0000) >> 16;
//			raw_x.main = data[i] & 0x03FF;
//
//			myfile << count << "," << raw_x.ref << "," << raw_x.main << std::endl;
////			raw_x_pub.publish(raw_x);
//		}
