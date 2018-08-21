# List of scripts

## Preprocessing scripts

* [preprocessing/dat2csv.py](https://github.com/arvpUofA/au_sonar/blob/data_processing/scripts/preprocessing/dat2csv.py) - Converts raw hex data files from the BBB to a CSV file.

## Test data loading scripts

* [load_data/load_Jan05.m](https://github.com/arvpUofA/au_sonar/blob/master/scripts/load_data/load_Jan05.m) - MATLAB script to load data from Jan05 test into MATLAB. *Note: this script does not load control data from test#4*.

## Gain simulator

* [simulator/sonar_sim.slx](https://github.com/arvpUofA/au_sonar/blob/master/scripts/simulator/sonar_sim.slx) - Contains a model for the hydrophone ping with 27000 kHz sampled at 500 kHz. The simulator also buffers and spits out data in 256 byte buffers to simulate actual conditions.

* [simulator/GainControl.m](https://github.com/arvpUofA/au_sonar/blob/master/scripts/simulator/GainControl.m) - Contains MATLAB object to simulate Automatic Gain Control for the simulator.
