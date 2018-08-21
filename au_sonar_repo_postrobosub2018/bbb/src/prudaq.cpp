#include "prudaq.h"

using namespace sonar;

Prudaq::Prudaq(int frequency, std::string pru0_path, std::string pru1_path)
{
	/*
	 * initialize PRU
	 */
	prussdrv_init();
	if(prussdrv_open(PRU_EVTOUT_0) != 0)
	{
		throw std::runtime_error("prussdrv_init() failed. Are you running as sudo?");
	}
	tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;
	prussdrv_pruintc_init(&pruss_intc_initdata);

	// Get pointer into the 8KB of shared PRU DRAM where prudaq expects
	// to share params with prus and the main cpu
	prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, (void**)&pparams);
	// Pointer into the DDR RAM mapped by the uio_pruss kernel module.
	prussdrv_map_extmem((void**)&shared_ddr);
	shared_ddr_len = prussdrv_extmem_size();
	unsigned int physical_address = prussdrv_get_phys_addr((void*)shared_ddr);

	// shared memory is slow so set up a local buffer to set up data
	local_buf = (uint32_t *) malloc(shared_ddr_len);
	if(!local_buf)
	{
		throw std::runtime_error("Couldn't allocate memory for local buffer.");
	}

	// use first 8 bytes of PRU memory to tell it location of shared segment of system memory
	pparams->physical_addr = physical_address;
	pparams->ddr_len       = shared_ddr_len;

	// Calculate the GPIO clock high and low cycle counts.
	// Adding 0.5 and truncating is equivalent to rounding
	int cycles = (PRU_CLK/frequency + 0.5);
	this->frequency = PRU_CLK/((float)cycles);
	pparams->high_cycles = cycles/2;
	pparams->low_cycles  = cycles - pparams->high_cycles;

	// set analog switches to select input (pru register r30)
	// 	channel 0
	// 		- 0 = 0
	//		- 1 = (1<<1)
	//		- 2 = (1<<2)
	//		- 3 = (1<<1) | (1<<2)
	//	channel 1
	// 		- 4 = 0
	//		- 5 = (1<<3)
	//		- 6 = (1<<5)
	//		- 7 = (1<<3) | (1<<5)
	// channel_0 = 0; channel_1 = 4
	// TODO: this will be controlled by the PRU for round robin
	pparams->input_select = 0;

	// Load the .bin files into PRU0 and PRU1
	prussdrv_exec_program(0, pru0_path.c_str());
	prussdrv_exec_program(1, pru1_path.c_str());

	// set up everything for the main loop
	max_index = shared_ddr_len / sizeof(shared_ddr[0]);
	time_t now = time(NULL);
	time_t start_time = now;
	int loops = 0;
}

Prudaq::~Prudaq()
{

}

uint32_t Prudaq::getData(uint32_t* data)
{
	// Reading from shared memory and PRU RAM is significantly slower than normal memory
	uint32_t *write_pointer_virtual = (uint32_t*)prussdrv_get_virt_addr(pparams->shared_ptr);
	uint32_t write_index = write_pointer_virtual - shared_ddr;

	uint32_t samples_read = 0;
	int bytes = 0;

	if (read_index == write_index)
	{
		// We managed to loop all the way back before PRU1 wrote even a single sample.
		//Do nothing.
	}
	else if (read_index < write_index)
	{
		// copy data into RAM
		samples_read = write_index - read_index;
		bytes = samples_read * sizeof(*shared_ddr);
		memcpy(local_buf, (void*) &(shared_ddr[read_index]), bytes);
		total_bytes_read += bytes;
	}
	else
	{
		// write pointer has wrapped around so we'll copy out the data in two chunks
		int tail_words = max_index - read_index;
		int tail_bytes = tail_words * sizeof(*shared_ddr);
		memcpy(local_buf, (void*)&(shared_ddr[read_index]), tail_bytes);
		total_bytes_read += tail_bytes;

		int head_bytes = write_index * sizeof(*shared_ddr);
		memcpy(&(local_buf[tail_words]), (void*)shared_ddr, head_bytes);
		total_bytes_read += head_bytes;
		bytes = tail_bytes + head_bytes;
		samples_read = tail_words + write_index;
	}

	read_index = write_index;

	// stats
	uint32_t bytes_written = pparams->bytes_written;
	int64_t difference = ((int64_t) bytes_written) - total_bytes_read;
	if (difference < 0) {
			difference = ((uint32_t) bytes_written + shared_ddr_len) - ((uint32_t) total_bytes_read + shared_ddr_len);
	}
//	std::cout << "written: " << bytes_written << std::endl;
//	std::cout << "diff: " << difference << std::endl;

	// return data
	for (int i = 0; i < samples_read; i++) {
		local_buf[i] &= 0x03ff03ff;
	}
	fwrite(local_buf, bytes, 1, fout);
	data = local_buf;
	return samples_read;
}

//
//#include <unistd.h>
//#include <stdlib.h>
//#include <stdio.h>

//#include <libgen.h>
//#include <string.h>
//
//
//#include <signal.h>
//#include <time.h>
//
//// Header for sharing info between PRUs and application processor
//#include "shared_header.h"
//
//
//// Used by sig_handler to tell us when to shutdown
//static int bCont = 1;
//

//
//void sig_handler (int sig) {
//  // break out of reading loop
//  bCont = 0;
//  return;
//}
//
//int main (int argc, char **argv) {
//  int ch = -1;
//  double gpiofreq = 1000;
//  int channel0_input = 0;
//  int channel1_input = 4;
//  char* fname = "-";
//  FILE* fout = stdout;
//
//
//
//  // Install signal handler to catch ctrl-C
//  if (SIG_ERR == signal(SIGINT, sig_handler)) {
//    perror("Warn: signal handler not installed %d\n");
//  }
//
//  fprintf(stderr,
//          "%uB of shared DDR available.\n Physical (PRU-side) address:%x\n",
//         shared_ddr_len, physical_address);
//  fprintf(stderr, "Virtual (linux-side) address: %p\n\n", shared_ddr);
//  if (shared_ddr_len < 1e6) {
//    fprintf(stderr, "Shared buffer length is unexpectedly small.  Buffer overruns"
//            " are likely at higher sample rates.  (Perhaps extram_pool_sz didn't"
//            " get set when uio_pruss kernel module loaded.  See setup.sh)\n");
//  }
//

//  while (bCont) {
//    read_index = write_index;
//
//    if (loops++ % 100 == 0) {
//      time_t current_time = time(NULL);
//      if (now != current_time) {
//        now = current_time;
//        // There's a race condition here where the PRU will often update bytes_written
//        // after we checked write_index, so don't worry about small differences. If the
//        // buffer overruns, we'll end up being off by an entire buffer worth.
//        uint32_t bytes_written = pparams->bytes_written;
//        int64_t difference = ((int64_t) bytes_written) - bytes_read;
//        if (difference < 0) {
//          difference = ((uint32_t) bytes_written + shared_ddr_len) -
//                       ((uint32_t) bytes_read + shared_ddr_len);
//        }
//
//        fprintf(stderr, "\t%ld bytes / second. %uB written, %uB read.\n",
//                bytes_written / (now - start_time), bytes_written, bytes_read);
//      }
//    }
//    usleep(100);
//  }
//
//
//  if (stdout != fout) {
//    fclose(fout);
//  }
//
//  return 0;
//}
