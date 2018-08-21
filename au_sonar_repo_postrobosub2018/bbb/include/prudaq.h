#include <iostream>
#include <stdexcept>
#include <cstring>
#include <inttypes.h>

#include <prussdrv.h>
#include <pruss_intc_mapping.h>

#include "shared_header.h"

namespace sonar
{

class Prudaq
{
public:
	/*
	 * initializes the DAQ by loading firmware to each PRU
	 * parameters:
	 * 	- frequency: sampling frequency
	 * 	- pru0_path: path to pru0 bin firmware file
	 * 	- pru1_path: path to pru1 bin firmware file
	 */
	Prudaq(int frequency, std::string pru0_path, std::string pru1_path);
	~Prudaq();

	/*
	 * gets data loop
	 * TODO: make this better
	 */
	uint32_t getData(uint32_t* data);

	// local memory buffer for data
	uint32_t* local_buf;


private:
	float frequency;
	const long PRU_CLK = 200e6;

	// memory map of shared values between PRU and Linux
	// shared_memory.h
	volatile pruparams_t *pparams = NULL;
	// pointer into the DDR RAM mapped by UIO
	volatile uint32_t *shared_ddr = NULL;
	unsigned int shared_ddr_len;
	// write pointer
	uint32_t read_index = 0;
	// number of bytes read in total
	uint32_t total_bytes_read = 0;
	// max_index of buffer. Used to set up the ring buffer
	uint32_t max_index;
	FILE* fout = stdout;

}; // end of Prudaq class

}; // end of sonar namespace
