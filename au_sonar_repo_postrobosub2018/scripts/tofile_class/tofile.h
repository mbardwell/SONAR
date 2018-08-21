//////////////////////////////////////////////
/*                 TO_FILE.H                */
//////////////////////////////////////////////

#ifndef TO_FILE_H
#define TO_FILE_H

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <ctime>
#include <vector>
using namespace std;

// Set defines to allocate proper matrix size in memory
#define PINGDELAY 2 // in seconds

typedef struct { // creating ping type
  vector<int> hydroA;
  vector<int> hydroB;
  vector<int> hydroC;
} ping_t;

class tofile {
private:
  string fs, line;
  double ** data;
  int iteration = 0, start = 0, elapsed = 0;
  int firstcall = 0;
  long count = 0, pingcount = 0;
  int nopings = 0; // Max number of pings
  int maxdatapoints = 0; // Max number of data points per ping
  vector<int> pingstats;
  vector<ping_t> data1;
  int hydrophone = 1;
  ping_t temp;

public:
  int _pingflag = 0;
  int _calibrationflag = 1;
  int _acqreadyflag = 1;
  int _gain = 0;
  int _peaklevel;
  tofile(string filename);
  ping_t * getData();
  void prepFile(string filename);
  void readFile(string filename);
};

#endif
