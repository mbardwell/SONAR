#include "Arduino.h"
#include "math.h"
#define FREQKHZ 45
#define BUFFERSIZE 8*(int)(2250000*20/(FREQKHZ*1000)/8)
#define BIAS (1.0*4096/3.3)
#define DC (1.8*4096/3.3)

static volatile uint16_t sinetable1[BUFFERSIZE];
void setup() {
  /* Waveform */
  // fill up the sine table
  for(int i=0; i<0.1*BUFFERSIZE; i++) {
    sinetable1[i] = BIAS+(int)(BIAS*sin(((float)i)*20.0*TWO_PI/((float)BUFFERSIZE)));
  }
  for(int i=0.1*BUFFERSIZE; i<BUFFERSIZE; i++) {
    sinetable1[i] = (BIAS) + (DC/8 - 0)*(float)rand()/RAND_MAX;
  }

  /* DAC */
  // initialise the DAC
  SIM_SCGC2 |= SIM_SCGC2_DAC0; // enable DAC clock
  DAC0_C0 = DAC_C0_DACEN | DAC_C0_DACRFS; // enable the DAC module, 3.3V reference
  // slowly ramp up to DC voltage
  for (int16_t i=0; i<BIAS; i+=1) {
    *(int16_t *)&(DAC0_DAT0L) = i;
    delayMicroseconds(125); // this function may be broken
  }
  // fill up the buffer with 2048
  for (int16_t i=0; i<16; i+=1) {
    *(int16_t *)(&DAC0_DAT0L + 2*i) = BIAS;//256*(16-i) - 1;
  }

  /* DMA */
  // initialise the DMA
  // first, we need to init the dma and dma mux
  // to do this, we enable the clock to DMA and DMA MUX using the system timing registers
  SIM_SCGC6 |= SIM_SCGC6_DMAMUX; // enable DMA MUX clock
  SIM_SCGC7 |= SIM_SCGC7_DMA;    // enable DMA clock
  // next up, the channel in the DMA MUX needs to be configured
  DMAMUX0_CHCFG0 |= DMAMUX_SOURCE_DAC0; //Select DAC as request source
  DMAMUX0_CHCFG0 |= DMAMUX_ENABLE;      //Enable DMA channel 0
  // then, we enable requests on our channel
  DMA_ERQ = DMA_ERQ_ERQ0; // Enable requests on DMA channel 0
  // Here we choose where our data is coming from, and where it is going
  DMA_TCD0_SADDR = sinetable1;   // set the address of the first byte in our LUT as the source address
  DMA_TCD0_DADDR = &DAC0_DAT0L; // set the first data register as the destination address
  // now we need to set the read and write offsets - kind of boring
  DMA_TCD0_SOFF = 4; // advance 32 bits, or 4 bytes per read
  DMA_TCD0_DOFF = 4; // advance 32 bits, or 4 bytes per write
  // this is the fun part! Now we get to set the data transfer size...
  DMA_TCD0_ATTR  = DMA_TCD_ATTR_SSIZE(DMA_TCD_ATTR_SIZE_32BIT); // Missing |=?
  DMA_TCD0_ATTR |= DMA_TCD_ATTR_DSIZE(DMA_TCD_ATTR_SIZE_32BIT) | DMA_TCD_ATTR_DMOD(31 - __builtin_clz(32)); // set the data transfer size to 32 bit for both the source and the destination
  // ...and the number of bytes to be transferred per request (or 'minor loop')...
  DMA_TCD0_NBYTES_MLNO = 16; // we want to fill half of the DAC buffer, which is 16 words in total, so we need 8 words - or 16 bytes - per transfer
  // set the number of minor loops (requests) in a major loop
  // the circularity of the buffer is handled by the modulus functionality in the TCD attributes
  DMA_TCD0_CITER_ELINKNO = DMA_TCD_CITER_ELINKYES_CITER(BUFFERSIZE*2/16);
  DMA_TCD0_BITER_ELINKNO = DMA_TCD_BITER_ELINKYES_BITER(BUFFERSIZE*2/16);
  // the address is adjusted by these values when a major loop completes
  // we don't need this for the destination, because the circularity of the buffer is already handled
  DMA_TCD0_SLAST    = -BUFFERSIZE*2;
  DMA_TCD0_DLASTSGA = 0;
  // do the final init of the channel
  DMA_TCD0_CSR = 0;
  // enable DAC DMA
  DAC0_C0 |= DAC_C0_DACBBIEN | DAC_C0_DACBWIEN; // enable read pointer bottom and waterwark interrupt
  DAC0_C1 |= DAC_C1_DMAEN | DAC_C1_DACBFEN | DAC_C1_DACBFWM(3); // enable dma and buffer
  DAC0_C2 |= DAC_C2_DACBFRP(0);
  // init the PDB for DAC interval generation
  SIM_SCGC6 |= SIM_SCGC6_PDB; // turn on the PDB clock
  PDB0_SC |= PDB_SC_PDBEN; // enable the PDB
  PDB0_SC |= PDB_SC_TRGSEL(15); // trigger the PDB on software start (SWTRIG)
  PDB0_SC |= PDB_SC_CONT; // run in continuous mode
  PDB0_MOD = 20-1; // modulus time for the PDB
  PDB0_DACINT0 = (uint16_t)(20-1); // we won't subdivide the clock...
  PDB0_DACINTC0 |= 0x01; // enable the DAC interval trigger
  PDB0_SC |= PDB_SC_LDOK; // update pdb registers
  PDB0_SC |= PDB_SC_SWTRIG; // ...and start the PDB
}

void loop() {

}
