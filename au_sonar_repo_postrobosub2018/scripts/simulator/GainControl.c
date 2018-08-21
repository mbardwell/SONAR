/* Gain control v1 written by Mike Bardwell 2018/02/23

   input: 256 byte "block" from 1 hydrophone
   outputs: Digital potentiometer value between 1:1000*

   Note: Linter approved. *Need to add char(hex) output
*/

// Include statements
// #include <GainControl.h> // Custom library
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

// Properties
#define ARRAYSIZE 257
#define MAXARRAYSIZE 1000000
#define INITIALGAIN 40
#define MAXGAIN 100
#define MINGAIN 1
#define KTHRESH 3
#define PINGHGTSAMPLES 5

unsigned long count = 0, step = 0, i = 0;
unsigned long threshold = 0, pinghgt, gain, sum; // Could be ints
unsigned int block[ARRAYSIZE], sorted_block[ARRAYSIZE], block_std[MAXARRAYSIZE];

float stddev(unsigned int *block, int blocksize) {
  int  i, n = blocksize/sizeof(*block);
  float average, variance, std_deviation, sum = 0, sum1 = 0;
  for (i = 0; i < n; i++)
  {
      sum = sum + block[i];
  }
  average = sum / (float)n;
  /*  Compute  variance and standard deviation  */
  for (i = 0; i < n; i++)
  {
      sum1 = sum1 + pow((block[i] - average), 2);
  }
  variance = sum1 / (float)n;
  std_deviation = sqrt(variance);
  return std_deviation;
}

int comp (const void * elem1, const void * elem2)
{
    int f = *((int*)elem1);
    int s = *((int*)elem2);
    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}

int main(int argc, char** argv) {
  if (step < 200) {
    block_std[step] = stddev(block, sizeof(block));
  }
  else if (step == 200) {
    int sum = 0;
    for(i = 0; i < step; i++) {
      sum = sum + block_std[i];
    }
    threshold = KTHRESH*sum/step;
  }
  else {
    if (threshold == 0) { // If threshold isn't set, restart
      step = 0;
    }
    block_std[step] = stddev(block, sizeof(block));
    if (block_std[step] > threshold) {
      qsort(block, sizeof(block)/sizeof(*block), sizeof(*block), comp);
      int sum = 0;
      for(i = 0; i < PINGHGTSAMPLES; i++) {
        sum = sum + block[i];
      }
      pinghgt = sum/PINGHGTSAMPLES;
      if (pinghgt > 1.9) {
        gain = gain/2;
      }
      else if (pinghgt < 1.5) {
        gain = gain*1.8/pinghgt;
      }
      count = 0; // Ping was detected, so reset counter
    }
    else {
      pinghgt = 0;
      count = count + 1;
    }
    if (gain < MINGAIN) {
      gain = 1;
    }
    else if (gain > MAXGAIN) {
      gain = 1000;
    }
  }
}
