#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include "LTC1865.h"

#define ADC_CH0_H 0x80
#define ADC_CH0_L 0x00
#define ADC_CH1_H 0xC0
#define ADC_CH1_L 0x00

#define CLOCK_SPEED 1000000

void LTC_init(uint8_t channel, uint8_t firstch)
{
	int fd;
	unsigned char buffer[2];

	fd = wiringPiSPISetup(channel, CLOCK_SPEED);
	printf("fd=%d\n",fd);
	if (fd == -1)
		printf("SPI failed");

	if (firstch)
	{
        buffer[0] = ADC_CH1_H;
        buffer[1] = ADC_CH1_L;
        wiringPiSPIDataRW(channel, buffer, 2);
	}
	else
	{
        buffer[0] = ADC_CH0_H;
        buffer[1] = ADC_CH0_L;
        wiringPiSPIDataRW(channel, buffer, 2);
	}
}

unsigned int LTC_Read(uint8_t channel, uint8_t nextch)
{
	unsigned char buffer[2];
	unsigned int data;

	delayMicroseconds(4);

	if (nextch)
	{
        buffer[0] = ADC_CH1_H;
        buffer[1] = ADC_CH1_L;
        wiringPiSPIDataRW(channel, buffer, 2);
	}
	else
	{
        buffer[0] = ADC_CH0_H;
        buffer[1] = ADC_CH0_L;
        wiringPiSPIDataRW(channel, buffer, 2);
	}
	data = buffer[0]<<8 | buffer[1];
	return data;
}
