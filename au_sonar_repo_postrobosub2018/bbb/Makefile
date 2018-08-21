CFLAGS += --std=c++11 -O2 -Wall

CC := g++
RM := $(RM)
PASM := pasm -DBUILD_WITH_PASM=1
DTC := dtc

SRC_DIR := src
FIRMWARE_DIR := firmware
INCLUDE_DIR := ./include

.PHONY: all clean install

TARGETS := sonar prudaq_capture $(FIRMWARE_DIR)/pru0.bin $(FIRMWARE_DIR)/pru1.bin

all: $(TARGETS)

clean:
		$(RM) $(TARGETS)
		
%.bin: %.p
		$(PASM) -I$(INCLUDE_DIR) -b $< $(basename $^)

prudaq_capture: $(SRC_DIR)/prudaq_capture.c
		$(CC) $(CFLAGS) -o $@ $^ -l prussdrv -I$(INCLUDE_DIR)
		
sonar: $(SRC_DIR)/sonar.cpp $(SRC_DIR)/prudaq.cpp
		$(CC) $(CFLAGS) -o $@ $^ -l prussdrv -I$(INCLUDE_DIR)