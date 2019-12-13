#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

/*
 * Macro Definitions
 */

//LTC1865
#define ADC_CH0_H   0x80
#define ADC_CH0_L   0x00
#define ADC_CH1_H   0xC0
#define ADC_CH1_L   0x00
#define CLOCK_SPEED 1000000

//C12880
#define SPEC_CLK_B       0  //gpio use wPi definition   //11 in PCB
#define SPEC_ST_B        2  //gpio use wPi definition   //13 in PCB
#define SPEC_CLK_A       21 //gpio use wPi definition   //29 in PCB
#define SPEC_ST_A        22 //gpio use wPi definition   //31 in PCB
#define SPEC_CHANNELS    288 // New Spec Channel
#define Period_Time      87

#if 0 //LED
//#define LED_Ctrl1         8  //gpio use wPi definition
#define LED_Ctrl1         26  //8  //gpio use wPi definition
#define LED_Ctrl2         1  //gpio use wPi definition
#define LED_Ctrl3         4  //gpio use wPi definition
#define LED_MAX_Current   30  //ma
#define LED_MAX_Step      32
#endif

//LTC1865
static uint8_t g_channel;

#if 1 //C12880
//uint16_t data[SPEC_CHANNELS];
enum{
  ABSameTime = 0,
  ATimeBig2B,
  BTimeBig2A,
};
#endif

//LTC1865
void LTC_Init(uint8_t a_channel, uint8_t firstch)
{
  int fd;
  unsigned char buffer[2];

  g_channel = a_channel;
  fd = wiringPiSPISetup(g_channel, CLOCK_SPEED);
  //printf("fd = %d\n",fd);
  //if (fd == -1)
    //printf("SPI failed");

  if (firstch)
  {
        buffer[0] = ADC_CH1_H;
        buffer[1] = ADC_CH1_L;
        wiringPiSPIDataRW(g_channel, buffer, 2);
  }
  else
  {
        buffer[0] = ADC_CH0_H;
        buffer[1] = ADC_CH0_L;
        wiringPiSPIDataRW(g_channel, buffer, 2);
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
        wiringPiSPIDataRW(g_channel, buffer, 2);
  }
  else
  {
        buffer[0] = ADC_CH0_H;
        buffer[1] = ADC_CH0_L;
        wiringPiSPIDataRW(g_channel, buffer, 2);
  }
  data = buffer[0]<<8 | buffer[1];
  return data;
}

#if 0 //LED
void LED_Init(int ctrl_pin)
{
  pinMode(ctrl_pin, OUTPUT);
  digitalWrite(ctrl_pin, LOW);
  delayMicroseconds(1500);

}

void LED_Set_Ctrl_Current(int ctrl_pin, int current)
{
  float LowCtrl = 0;
  int i = 0;

  if (current > LED_MAX_Current)
  {
    current = LED_MAX_Current;
  }
  else
  {
    LowCtrl = (float) ( LED_MAX_Current - current ) * LED_MAX_Step / LED_MAX_Current + 0.5;
  }
  //printf("LED step = %f\n", LowCtrl);

  digitalWrite(ctrl_pin, LOW);
  delayMicroseconds(1500);

  if (current > 0)
  {
    digitalWrite(ctrl_pin, HIGH);
    delayMicroseconds(1);

    for (i = 1; i <= LowCtrl; i++)
    {
      digitalWrite(ctrl_pin, LOW);
      delayMicroseconds(1);
      digitalWrite(ctrl_pin, HIGH);
      delayMicroseconds(1);
      //printf("%d-", i);
    }
    //printf("\n");
  }

}

void LED_Set_Current(int led, int current)
{
  if (led == 3)
    LED_Set_Ctrl_Current(LED_Ctrl3, current);
  else if (led == 2)
    LED_Set_Ctrl_Current(LED_Ctrl2, current);
  else
    LED_Set_Ctrl_Current(LED_Ctrl1, current);
}
#endif

//C12880
void Setup()
{
  wiringPiSetup() ;
  //Set desired pins to OUTPUT
  pinMode(SPEC_CLK_A, OUTPUT);
  pinMode(SPEC_ST_A, OUTPUT);
  pinMode(SPEC_CLK_B, OUTPUT);
  pinMode(SPEC_ST_B, OUTPUT);
  //pinMode(LASER_404, OUTPUT);
  

  digitalWrite(SPEC_CLK_A, HIGH); // Set SPEC_CLK High
  digitalWrite(SPEC_ST_A, LOW); // Set SPEC_ST Low
  digitalWrite(SPEC_CLK_B, HIGH); // Set SPEC_CLK High
  digitalWrite(SPEC_ST_B, LOW); // Set SPEC_ST Low

  //LTC1865
  LTC_Init(0, 0);
#if 0  //LED
  LED_Init(LED_Ctrl1);
  LED_Init(LED_Ctrl2);
  LED_Init(LED_Ctrl3);
#endif

}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */

void Read2Spectrometer(unsigned long Int_timeA, unsigned long Int_timeB, unsigned int * dataA, unsigned int * dataB)
{
  int delayTime = 1, counter = 0; // delay time
  long startTime = 0;
  unsigned long Int_timeBothAB, P_timeBothAB;
  uint8_t ucFlagAB;

  if (Int_timeA > Int_timeB)
  {
    Int_timeBothAB = Int_timeB;
    Int_timeA -= Int_timeB;
    ucFlagAB = ATimeBig2B;
  }
  else if (Int_timeB > Int_timeA)
  {
    Int_timeBothAB = Int_timeA;
    Int_timeB -= Int_timeA;
    ucFlagAB = BTimeBig2A;
  }
  else //if (Int_timeA == Int_timeB)
  {
    Int_timeBothAB = Int_timeA;
    ucFlagAB = ABSameTime;
  }

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK_A, LOW);
  digitalWrite(SPEC_CLK_B, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK_A, HIGH);
  digitalWrite(SPEC_CLK_B, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK_A, LOW);
  digitalWrite(SPEC_CLK_B, LOW);
  digitalWrite(SPEC_ST_A, HIGH);
  digitalWrite(SPEC_ST_A, HIGH);
  delayMicroseconds(delayTime);

  //Sample for a small amount of time
  for (int i = 0; i < 7; i++)
  {
      digitalWrite(SPEC_CLK_A, HIGH);
      digitalWrite(SPEC_CLK_B, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_A, LOW);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime); 
  }

  //startTime = millis();
  startTime = micros();
  //printf("startTime = %d\n",startTime);
  //Sample for a period of time
  //for(int i = 0; i < 15; i++)
  counter = 0;

  while ( (micros() - startTime) <= Int_timeBothAB )
  {
      counter++;
      digitalWrite(SPEC_CLK_A, HIGH);
      digitalWrite(SPEC_CLK_B, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_A, LOW);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime); 
  }

  if (ucFlagAB == ATimeBig2B)
  {
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST_B, LOW);
    startTime = micros();
    while ( (micros() - startTime) <= Int_timeA )
    {
      counter++;
      digitalWrite(SPEC_CLK_A, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_A, LOW);
      delayMicroseconds(delayTime); 
    }
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST_A, LOW);
  }
  else if (ucFlagAB == BTimeBig2A)
  {
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST_A, LOW);
    startTime = micros();
    while ( (micros() - startTime) <= Int_timeB )
    {
      counter++;
      digitalWrite(SPEC_CLK_B, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime); 
    }
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST_B, LOW);
  }
  else //if (ucFlagAB == ABSameTime)
  {
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST_A, LOW);
    digitalWrite(SPEC_ST_B, LOW);
  }

  //printf("endTime = %d\n",millis());
  //printf("counter = %d\n", counter);


  //Sample for a period of time
  for(int i = 0; i < Period_Time; i++)
  {
      digitalWrite(SPEC_CLK_A, HIGH);
      digitalWrite(SPEC_CLK_B, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_A, LOW);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime); 
  }

  //Read from SPEC_VIDEO
  for(int i = 0; i < SPEC_CHANNELS; i++)
  {
      //data[i] = analogRead(SPEC_VIDEO);
      dataA[i] = LTC_Read(0);
      //printf("%d, ", dataA[i]);
      digitalWrite(SPEC_CLK_A, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_A, LOW);
      delayMicroseconds(delayTime);     

      dataB[i] = LTC_Read(1);
      //printf("%d, ", dataB[i]);
      digitalWrite(SPEC_CLK_B, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime);     
  }

  //printf("\n");
}

