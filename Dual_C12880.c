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
#define ADC_NEXT_CH_A  1
#define ADC_NEXT_CH_B  0

//C12880
#define SPEC_CLK_B       0  //gpio use wPi definition   //11 in PCB
#define SPEC_ST_B        2  //gpio use wPi definition   //13 in PCB
#define SPEC_CLK_A       21 //gpio use wPi definition   //29 in PCB
#define SPEC_ST_A        22 //gpio use wPi definition   //31 in PCB
#define SPEC_CHANNELS    288 // New Spec Channel
#define Period_Time      87

//LTC1865
static uint8_t g_channel;

#if 0 //C12880
uint16_t data[SPEC_CHANNELS];
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
  LTC_Init(0, ADC_NEXT_CH_A);

}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */

void Read2Spectrometer(unsigned long Int_timeA, unsigned long Int_timeB, unsigned int * dataA, unsigned int * dataB)
{
  int delayTime = 1, counter = 0; // delay time
  long startTime = 0, diffTime = 0;
  int P_timeA = 0, P_timeB = 0;

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
  digitalWrite(SPEC_ST_B, HIGH);
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

  diffTime = micros() - startTime;
  while ( ( diffTime <= Int_timeA ) || (P_timeA < Period_Time)
   || ( diffTime <= Int_timeB ) || (P_timeB < Period_Time) )
  {
      counter++;

      if ( diffTime >= Int_timeA )
      {
        //Set SPEC_ST to low
        if (P_timeA == 0)
        {
          digitalWrite(SPEC_ST_A, LOW);
          //printf("ST A low\n");
        }
        if (P_timeA < Period_Time)
        {
          digitalWrite(SPEC_CLK_A, HIGH);
          delayMicroseconds(delayTime);
          digitalWrite(SPEC_CLK_A, LOW);
          delayMicroseconds(delayTime); 
          //if (P_timeA > 0)
          //printf("A pulse = %d\n", P_timeA);
        }
        //else if (P_timeA == Period_Time)
        //{
          //printf("P_timeA Stop\n");
        //}
        P_timeA++;
      }
      else
      {
        digitalWrite(SPEC_CLK_A, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK_A, LOW);
        delayMicroseconds(delayTime);
        //printf("A pulse within int\n");
      }

      if ( diffTime >= Int_timeB )
      {
        //Set SPEC_ST to low
        if (P_timeB == 0)
        {
          digitalWrite(SPEC_ST_B, LOW);
          //printf("ST B low\n");
        }
        if (P_timeB < Period_Time)
        {
          digitalWrite(SPEC_CLK_B, HIGH);
          delayMicroseconds(delayTime);
          digitalWrite(SPEC_CLK_B, LOW);
          delayMicroseconds(delayTime); 
          //if (P_timeB > 0)
          //printf("B pulse = %d\n", P_timeB);
        }
        //else if (P_timeB == Period_Time)
        //{
          //printf("P_timeB Stop\n");
        //}
        P_timeB++;
      }
      else
      {
        digitalWrite(SPEC_CLK_B, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK_B, LOW);
        delayMicroseconds(delayTime); 
        //printf("B pulse within int\n");
      }
      diffTime = micros() - startTime;
  }

  //printf("endTime = %d\n",millis());
  //printf("counter = %d\n", counter);

  //Read from SPEC_VIDEO
  for(int i = 0; i < SPEC_CHANNELS; i++)
  {
      //data[i] = analogRead(SPEC_VIDEO);

      digitalWrite(SPEC_CLK_A, HIGH);
      digitalWrite(SPEC_CLK_B, HIGH);
      dataA[i] = LTC_Read(ADC_NEXT_CH_B);
      dataB[i] = LTC_Read(ADC_NEXT_CH_A);
      //printf("%d, ", dataA[i]);
      //printf("%d, ", dataB[i]);
      digitalWrite(SPEC_CLK_A, LOW);
      digitalWrite(SPEC_CLK_B, LOW);
      delayMicroseconds(delayTime);     

  }

  //printf("\n");
}

