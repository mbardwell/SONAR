#include <iostream>
#include <sstream>
#include <ios>
#include "mcp4561.hpp"

void usage()
{
	std::cerr << "Usage: ./amp_test address <value> [if no value is provided it reads the pot" << std::endl;
}

int read_address(char* argument)
{
	std::stringstream ss(argument); ss << std::hex;
	int address;
	if(!(ss >> address) or !(address == 46 or address == 47))
	{
		std::stringstream e_msg;
		e_msg << "Wrong address provided: 0x" << std::hex << address << ". Address can only be 0x2e/0x2f";
		throw std::invalid_argument( e_msg.str() );
	}
	return address;
}

int read_value(char* argument)
{
	std::stringstream ss(argument);
	int value;
	if(!(ss >> value) or value < 0 or value > 256)
	{
		std::stringstream e_msg;
		e_msg << "Wrong value provided for Pot: " << value << ". Value should be between 0-256(inclusive).";
		throw std::invalid_argument( e_msg.str() );
	}
	return value;
}

int main(int argc, char** argv)
{
	mcp4561::MCP4561 *pot;
	int address;

	if(argc == 2 or argc == 3)
	{
		// initialize
		try
		{
			address = read_address(argv[1]);
			// initialize device
			pot = new mcp4561::MCP4561(address);
		}
		catch(mcp4561::InitializationException& e)
		{
			std::cerr << "Error: I2C not initialized - " << e.what() << "\nEXITING" << std::endl;
			delete pot;
			return 1;
		}
		catch(std::invalid_argument& e)
		{
			std::cerr << "Error: " << e.what() << "\nEXITING..." << std::endl;
			return 1;
		}

		if(argc == 2)
		{
			// read mode
			try
			{
				std::cout << "Pot:0x" << std::hex << address << " has value of " << std::dec << pot->get_pot() << std::endl;
			}
			catch(std::exception& e)
			{
				std::cerr << "Error: " << e.what() << "\nEXITING" << std::endl;
				delete pot;
				return 1;
			}
		}

		if(argc == 3)
		{
			int value;
			// write mode
			try
			{
				value = read_value(argv[2]);
				pot->set_pot(value);
				std::cout << "Wrote value: " << value << " to pot:0x" << std::hex << address << std::endl;
			}
			catch(std::exception& e)
			{
				std::cerr << "Error: " << e.what() << "\nEXITING..." << std::endl;
				delete pot;
				return 1;
			}
		}
	}
	else
	{
		// correct params not provided
		usage();
		return 1;
	}

	delete pot;
	return 0;
}
