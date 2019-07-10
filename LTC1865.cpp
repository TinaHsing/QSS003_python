#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include "LTC1865.h"

//void LTC1865::init(uint8_t channel, uint8_t convpin, uint8_t firstch)
void LTC_init(uint8_t channel, uint8_t firstch)
{
   	int fd, result;
   	unsigned char buffer[100];

	_channel = channel;
	//_convpin = convpin;

	//pinMode(_convpin, OUTPUT);
	//digitalWrite(_convpin, LOW);
	pinMode(_channel, OUTPUT);
	digitalWrite(_channel, LOW);
   	fd = wiringPiSPISetup(_channel, CLOCK_SPEED);

	if(firstch)
	{
    	buffer[0] = ADC_CH1_H;
    	buffer[1] = ADC_CH1_L;
    	result = wiringPiSPIDataRW(_channel, buffer, 2);
	}
	else
	{
    	buffer[0] = ADC_CH0_H;
    	buffer[1] = ADC_CH0_L;
    	result = wiringPiSPIDataRW(_channel, buffer, 2);
	}
}

unsigned int LTC_Read(uint8_t nextch)
{
   	int data;
   	unsigned char buffer[100];

	//digitalWrite(_convpin, HIGH);
	digitalWrite(_channel, HIGH);
	delayMicroseconds(4);
	//digitalWrite(_convpin, LOW);
	digitalWrite(_channel, LOW);

	if (nextch)
	{
    	buffer[0] = ADC_CH1_H;
    	buffer[1] = ADC_CH1_L;
    	data = wiringPiSPIDataRW(_channel, buffer, 2);
	}
	else
	{
    	buffer[0] = ADC_CH0_H;
    	buffer[1] = ADC_CH0_L;
    	data = wiringPiSPIDataRW(_channel, buffer, 2);
	}
	return data;
}