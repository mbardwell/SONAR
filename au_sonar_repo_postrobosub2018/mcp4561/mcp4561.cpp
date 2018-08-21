#include "mcp4561.hpp"

#include <iostream>
#include <cstdio>
#include <sstream>
#include <stdexcept>

#include <unistd.h> /* for socket handling open(), close() */
#include <fcntl.h>	/* for O_RDWR */
#include <sys/ioctl.h>	/* for ioctl */
#include <linux/i2c-dev.h> /* for I2C_SLAVE */

using namespace mcp4561;

MCP4561::MCP4561(int address)
: MCP4561(2, address)
{
}

MCP4561::MCP4561(int bus, int address)
: is_init(false), i2c_handler(0)
{
	try
	{
		i2c_handler = initialize_i2c(bus, address);
	}
	catch (InitializationException& e)
	{
		throw e;
	}
	is_init = true;
	bool test = test_connection();
	if(test)
	{
		std::cout << "Connection i2c-" << bus << " @ address 0x" << std::hex << address << std::dec << " initialized" << std::endl;
	}
	else
	{
		is_init = false;
		throw InitializationException("Connection test failed.");
	}
}

MCP4561::~MCP4561()
{
	close(i2c_handler);
}

int MCP4561::initialize_i2c(int bus, int address)
{
	char connection_path[12];
	snprintf(connection_path, sizeof(connection_path), "/dev/i2c-%d", bus);

	int file_h;
	if((file_h = open(connection_path, O_RDWR)) < 0)
	{
		std::stringstream error_message;
		error_message << "failed to open " << connection_path << " connection";
		throw InitializationException(error_message.str());
	}
	if( ioctl(file_h, I2C_SLAVE, address) < 0 ) {
		std::stringstream error_message;
		error_message << "failed to connect to device @ address 0x" << std::hex << address;
		throw InitializationException(error_message.str());
	}
	return file_h;
}

unsigned char MCP4561::get_cmd(int address, int mode, int data)
{
	if( address < 0 or address >= 16)
	{
		throw std::invalid_argument("memory address should be between 0 and 15 (inclusive)");
	}
	if( mode < 0 or mode >= 4)
	{
		throw std::invalid_argument("invalid data access mode");
	}
	if( data < 0 or data > 257)
	{
		throw std::invalid_argument("data should be within 0 and 257 (inclusive)");
	}
	unsigned char cmd_byte = (address << 4) | (mode << 2) | ((data >> 8) & 0x03);
	return cmd_byte;
}

void MCP4561::set_pot(int value)
{
	try
	{
		write_register(static_cast<int>(MemoryAddress::wiper_reg), value);
		int data = read_register(static_cast<int>(MemoryAddress::wiper_reg));
		if(value != data)
		{
			throw IOException("written and read pot values do not match");
		}
	}
	catch(mcp4561::IOException& e)
	{
		throw e;
	}
	catch(mcp4561::InitializationException& e)
	{
		throw e;
	}
}

int MCP4561::get_pot()
{
	try
	{
		int data = read_register(static_cast<int>(MemoryAddress::wiper_reg));
		return data;
	}
	catch(mcp4561::IOException& e)
	{
		throw e;
	}
	catch(mcp4561::InitializationException& e)
	{
		throw e;
	}
}

void MCP4561::write_register(int memory_address, int data)
{
	if(not is_init) throw InitializationException("Cannot write because uninitialized.");
	unsigned char buf[2];
	try
	{
		buf[0] = get_cmd(memory_address, static_cast<int>(CommandMode::write), data);
		buf[1] = data & 0xFF;
	}
	catch( std::invalid_argument& e)
	{
		std::stringstream error_message;
		error_message << "write error due to invalid command parameters - " << e.what();
		throw IOException(error_message.str());
	}

	if(write(i2c_handler, buf, 2) != 2)
	{
		std::stringstream error_message;
		error_message << "error writing 0x" << std::hex << data << " to memory 0x" << memory_address << std::dec;
		throw IOException(error_message.str());
	}
}

int MCP4561::read_register(int memory_address)
{
	if(not is_init) throw InitializationException("Cannot read because uninitialized.");
	unsigned char buf[2];
	try
	{
		buf[0] = get_cmd(memory_address, static_cast<int>(CommandMode::read), 0);
	}
	catch( std::invalid_argument& e)
	{
		std::stringstream error_message;
		error_message << "read error due to invalid command parameters - " << e.what();
		throw IOException(error_message.str());
	}

	if(write(i2c_handler, buf, 1) != 1)
	{
		std::stringstream error_message;
		error_message << "error reading from memory 0x" << std::hex << memory_address << std::dec;
		throw IOException(error_message.str());
	}

	if(read(i2c_handler, buf, 2) != 2) {
		std::stringstream error_message;
		error_message << "error reading from memory 0x" << std::hex << memory_address << std::dec;
		throw IOException(error_message.str());
		std::cerr << "error reading" << std::endl;
	}
	else
	{
		return (static_cast<unsigned int>(buf[0]) << 8) | buf[1];
	}
}

bool MCP4561::test_connection()
{
	try
	{
		int data = read_register(static_cast<int>(MemoryAddress::status_reg));
		if((data >> 4) == 0b11111)
		{
			return true;
		}
		return false;
	}
	catch(mcp4561::IOException& e)
	{
		return false;
	}
	catch(mcp4561::InitializationException& e)
	{
		return false;
	}
}
