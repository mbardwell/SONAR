#ifndef MCP4561_H_
#define MCP4561_H_

#include <string>
#include <exception>

namespace mcp4561
{

enum class CommandMode {
	write = 0,
	increment = 1,
	decrement = 2,
	read = 3
};

enum class MemoryAddress {
	wiper_reg = 0x00,
	tcon_reg = 0x04,
	status_reg = 0x05
};

class MCP4561 {
public:
	/*
	 * initializes the device (assumes i2c-bus=1)
	 */
	MCP4561(int address);

	/*
	 * initializes the device with on i2c bus and address
	 */
	MCP4561(int bus, int address);

	/*
	 * closes the device connection and cleans up memory
	 */
	~MCP4561();

	/*
	 * sets the value of pot
	 */
	void set_pot(int value);

	/*
	 * gets the value of pot
	 */
	int get_pot();

	/*
	 * write data to a register.
	 * throws InitializationException and IOException
	 */
	void write_register(int memory_address, int data);

	/*
	 * read data from a register.
	 * throws InitializationException and IOException
	 * returns 9-bit data
	 */
	int read_register(int memory_address);

private:
	bool is_init;		/* set if device has been successfully initialized */
	int i2c_handler;	/* file handler for the i2c device */

	/*
	 * initializes the i2c connection and returns the connection handler
	 * throws InitializationException
	 */
	int initialize_i2c(int bus, int address);

	/*
	 * create the command byte
	 */
	unsigned char get_cmd(int address, int mode, int data = 0);

	/*
	 * reads status register to check if connection successful
	 */
	bool test_connection();
};

/*
 * Exception to deal with initialization issues
 */
class InitializationException : public std::exception
{
public:
	InitializationException(const std::string& message) : message_(message) {}
	virtual const char* what() const throw() {
		return message_.c_str();
	}
private:
	std::string message_;
};

/*
 * Exception to deal with I/O issues
 */
class IOException : public std::exception
{
public:
	IOException(const std::string& message) : message_(message) {}
	virtual const char* what() const throw() {
		return message_.c_str();
	}
private:
	std::string message_;
};

}

#endif
