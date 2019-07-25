#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <stdio.h>
#include "LTC1865.h"

//void LTC1865::init(uint8_t channel, uint8_t convpin, uint8_t firstch)

void LTCtest()
{
	printf("hello");
}

void LTC_init(uint8_t channel, uint8_t firstch)
{
   	int fd, result;
   	unsigned char buffer[100];



   	fd = wiringPiSPISetup(channel, CLOCK_SPEED);

	if(firstch)
	{
    	buffer[0] = ADC_CH1_H;
    	buffer[1] = ADC_CH1_L;
    	result = wiringPiSPIDataRW(channel, buffer, 2);
	}
	else
	{
    	buffer[0] = ADC_CH0_H;
    	buffer[1] = ADC_CH0_L;
    	result = wiringPiSPIDataRW(channel, buffer, 2);
	}
}

unsigned int LTC_Read(uint8_t channel, uint8_t nextch)
{
   	int data;
   	unsigned char buffer[100];



	delayMicroseconds(4);



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