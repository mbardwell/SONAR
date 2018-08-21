//////////////////////////////////////////////
/*                TO_FILE.CPP               */
//////////////////////////////////////////////

#include "tofile.h"

tofile::tofile(string filename) {
  readFile(filename);
  start = clock(); // start the timer
}

void tofile::readFile(string filename) {
  ifstream infile(filename);
  getline(infile, line); // pull first line for Fs
  while (getline(infile, line)) {
    if (line == "Ping Detected") {
      pingcount++; count = 0;
      // cout << "ping count: " << pingcount << endl; // debug
      hydrophone = 1;
      if (firstcall == 0) firstcall++;
      else {
        data1.push_back(temp);
        temp.hydroA.clear();
        temp.hydroB.clear();
        temp.hydroC.clear();
      }
    }
    else if (line == "") {
      count = 0;
      hydrophone++;
    }
    else {
      count++;
      // cout << "count: " << count << endl; // debug
      switch (hydrophone) {
        case 1:
          temp.hydroA.push_back(stod(line));
          // cout << "line A: " << temp.hydroA[count-1] << endl; // debug
          break;
        case 2:
          temp.hydroB.push_back(stod(line));
          // cout << "line B: " << temp.hydroB[count-1] << endl; // debug
          break;
        case 3:
          temp.hydroC.push_back(stod(line));
          // cout << "line C: " << temp.hydroC[count-1] << endl; // debug
          break;
      }
    }
  }
  data1.push_back(temp);
}

ping_t * tofile::getData() {
  elapsed = (clock() - start) / 1000; // in s
  // cout << "clock: " << clock() << " elapsed: " << elapsed << endl;
  if (elapsed < PINGDELAY) {
    _pingflag = 0;
  }
  else {
    _pingflag = 1;
    start = clock();
    // cout << "iteration: " << iteration << endl; // debug
    return &data1[iteration++];
  }
  return NULL;
}

int main() {
  // Testing code
  tofile test("C:/Users/Michael/Documents/au_sonar/scripts/tofile_class/processeddata.txt");
  clock_t clockstart = clock();
  ping_t * a = test.getData(); // ping not available yet, should read garbage
  int ping = 0;
  if (a == NULL) cout << "NULL Value" << endl;
  else {
    for (int i = 0; i < (int) a[0].hydroA.size(); i++) {
      cout << "hydroA: " << a[0].hydroA[i] << endl;

    }
    ping++;
  }
  while ((clock() - clockstart)/1000 < 2.1) {} // should read a ping
  a = test.getData();
  if (a == NULL) cout << "NULL Value" << endl;
  else {
    for (int i = 0; i < (int) a[0].hydroA.size(); i++) {
      cout << "hydroA: " << a[0].hydroA[i] << endl;
    }
    ping++;
  }
  while ((clock() - clockstart)/1000 < 4.5) {} // should be garbages
  a = test.getData();
  if (a == NULL) cout << "NULL Value" << endl;
  else {
    for (int i = 0; i < (int) a[0].hydroB.size(); i++) {
      cout << "hydroB: " << a[0].hydroB[i] << endl;
    }
    ping++;
  }
}
