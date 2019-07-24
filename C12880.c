#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <lcd.h>

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

//LED
#define LED_MAX_Current   30  //ma
#define LED_MAX_Step      32

//LCD
#define LCD_Rows    2
#define LCD_Cols    16
#define LCD_BITS    4
#define LCD_RS      9
#define LCD_STRB    7
#define LCD_D0      3
#define LCD_D1      0
#define LCD_D2      21
#define LCD_D3      2

//LTC1865
static uint8_t g_channel;

//LCD
static int g_lcdHandle;

//C12880
//uint16_t data[SPEC_CHANNELS];
static unsigned char SPEC_ST, SPEC_CLK, SPEC_VIDEO, WHITE_LED;

//LTC1865
void LTC_Init(uint8_t a_channel, uint8_t firstch)
{
  int fd;
  unsigned char buffer[2];

  g_channel = a_channel;
  fd = wiringPiSPISetup(g_channel, CLOCK_SPEED);
  printf("fd = %d\n",fd);
  if (fd == -1)
    printf("SPI failed");

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

//LED
void LED_Init(int ctrl_pin)
{
  digitalWrite(ctrl_pin, LOW);
  delayMicroseconds(1.5);

}

void LED_Set(int ctrl_pin, int current)
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
  printf("LED step = %f\n", LowCtrl);

  digitalWrite(ctrl_pin, LOW);
  delayMicroseconds(1500);
  digitalWrite(ctrl_pin, HIGH);
  delayMicroseconds(1);

  for (i = 1; i <= LowCtrl; i++)
  {
    digitalWrite(ctrl_pin, LOW);
    delayMicroseconds(1);
    digitalWrite(ctrl_pin, HIGH);
    delayMicroseconds(1);
    printf("%d-", i);
  }
  printf("\n");

}

//LCD
void LCD_Init()
{
  //4-bit
  g_lcdHandle = lcdInit(LCD_Rows, LCD_Cols, LCD_BITS, LCD_RS, LCD_STRB, LCD_D0, LCD_D1, LCD_D2, LCD_D3, 0, 0, 0, 0) ;

  if (g_lcdHandle < 0)
  {
    printf ("lcdInit failed\n") ;
  }

}

void LCD_clear()
{
  lcdClear(g_lcdHandle);
}

void LCD_Write(int x, int y, char *string)
{
  lcdPosition(g_lcdHandle, x, y);
  lcdPuts(g_lcdHandle, string);
}

//C12880
void Setup(unsigned char a_SPEC_ST, unsigned char a_SPEC_CLK, unsigned char a_SPEC_VIDEO, unsigned char a_WHITE_LED)
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
  LTC_Init(0, 0);  

}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */
void ReadSpectrometer(int delayTime, unsigned long Int_time, unsigned int * data)
{
  //int delayTime = 1; // delay time
  long startTime = 0;

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);

  startTime = millis();
  printf("startTime = %d\n",startTime);
  //Sample for a period of time
  //for(int i = 0; i < 15; i++)
  while ( (millis() - startTime) <= Int_time )
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }
  printf("endTime = %d\n",millis());

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

