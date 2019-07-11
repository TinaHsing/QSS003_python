#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

/*
 * Macro Definitions
 */
//#define SPEC_TRG         A0
//#define SPEC_ST          A1
//#define SPEC_CLK         A2
//#define SPEC_VIDEO       A3
//#define WHITE_LED        A4
//#define LASER_404        A5

//LTC1865
#define ADC_CH0_H 1
#define ADC_CH0_L 2
#define ADC_CH1_H 0xC0
#define ADC_CH1_L 0x00
#define CLOCK_SPEED 1000000

//C12880
#define SPEC_CHANNELS    288 // New Spec Channel

//LTC1865
uint8_t channel;

//C12880
//uint16_t data[SPEC_CHANNELS];
unsigned char SPEC_ST, SPEC_CLK, SPEC_VIDEO, WHITE_LED;

void LTC_init(uint8_t a_channel, uint8_t firstch)
{
  int fd;
  unsigned char buffer[2];

  channel = a_channel;
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

unsigned int LTC_Read(uint8_t nextch)
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

void setup(unsigned char a_SPEC_ST, unsigned char a_SPEC_CLK, unsigned char a_SPEC_VIDEO, unsigned char a_WHITE_LED)
{
  SPEC_ST = a_SPEC_ST;
  SPEC_CLK = a_SPEC_CLK;
  SPEC_VIDEO = a_SPEC_VIDEO;
  WHITE_LED = a_WHITE_LED;

  wiringPiSetup() ;
  //Set desired pins to OUTPUT
  pinMode(SPEC_CLK, OUTPUT);
  pinMode(SPEC_ST, OUTPUT);
  //pinMode(LASER_404, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);

  digitalWrite(SPEC_CLK, HIGH); // Set SPEC_CLK High
  digitalWrite(SPEC_ST, LOW); // Set SPEC_ST Low

  //LTC1865
  LTC_init(0, 0);  
}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */
void readSpectrometer(unsigned long Int_time, unsigned int * data)
{
  int delayTime = 1; // delay time

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);

  //Sample for a period of time
  for(int i = 0; i < 15; i++)
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

  //Set SPEC_ST to low
  digitalWrite(SPEC_ST, LOW);

  //Sample for a period of time
  for(int i = 0; i < 85; i++)
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

  //One more clock pulse before the actual read
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);

  //Read from SPEC_VIDEO
  for(int i = 0; i < SPEC_CHANNELS; i++)
  {
      //data[i] = analogRead(SPEC_VIDEO);
      data[i] = LTC_Read(0);
  
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime);     
  }

  //Set SPEC_ST to high
  digitalWrite(SPEC_ST, HIGH);

  //Sample for a small amount of time
  for(int i = 0; i < 7; i++)
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);

}

/*
 * The function below prints out data to the terminal or 
 * processing plot
 */
void printData()
{
  for (int i = 0; i < SPEC_CHANNELS; i++)
  {
    printf("%d",data[i]);
    printf(",");
  }
  printf("\n");
}

void loop()
{
  readSpectrometer(10);
  printData();
  delay(10);  
}

