#define ADC_CH0_H 0x80
#define ADC_CH0_L 0x00
#define ADC_CH1_H 0xC0
#define ADC_CH1_L 0x00

#define CLOCK_SPEED 1000000

class LTC1865
{
private: 
	uint8_t _convpin;
	uint8_t _channel;

public:
	LTC1865();
	void init(uint8_t channel, uint8_t convpin, uint8_t firstch);
	unsigned int Read(uint8_t nextch);
};
