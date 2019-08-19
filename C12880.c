#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
//#include <lcd.h>

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
#define SPEC_ST          22
#define SPEC_CLK         23
#define SPEC_CHANNELS    288 // New Spec Channel
#define Period_Time      87

//LED
//#define LED_Ctrl1         8  //gpio use wPi definition
#define LED_Ctrl1         26  //8  //gpio use wPi definition
#define LED_Ctrl2         1  //gpio use wPi definition
#define LED_Ctrl3         4  //gpio use wPi definition
#define LED_MAX_Current   30  //ma
#define LED_MAX_Step      32

#if 0 //LCD
#define LCD_Rows    2
#define LCD_Cols    16
#define LCD_BITS    4
#define LCD_RS      9   //gpio use wPi definition
#define LCD_STRB    7   //gpio use wPi definition
#define LCD_D0      3   //gpio use wPi definition
#define LCD_D1      0   //gpio use wPi definition
#define LCD_D2      21  //gpio use wPi definition
#define LCD_D3      2   //gpio use wPi definition
#endif

//LTC1865
static uint8_t g_channel;

#if 0 //LCD
static int g_lcdHandle;
//static char g_String[17];
#endif

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

//LED
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

#if 0 //LCD
void LCD_Init()
{
  //4-bit
  g_lcdHandle = lcdInit(LCD_Rows, LCD_Cols, LCD_BITS, LCD_RS, LCD_STRB, LCD_D0, LCD_D1, LCD_D2, LCD_D3, 0, 0, 0, 0) ;

  //if (g_lcdHandle < 0)
    //printf ("LCD_Init failed\n") ;

}

void LCD_Clear()
{
  //printf("lcd = %d\n", g_lcdHandle);
  lcdClear(g_lcdHandle);
}

void LCD_Write(int x, int y, unsigned char *a_string)
{
  //printf("lcd = %d\n", g_lcdHandle);
  printf("%s\n", a_string);
  //sprintf(g_String, "%s", a_string);
  //printf("%s\n", g_String);
  lcdPosition(g_lcdHandle, x, y);
  delayMicroseconds(100);
  lcdPuts(g_lcdHandle, a_string);
  //lcdPuts(g_lcdHandle, g_String);
}

void LCD_Test(int j)
{
  char String[17];
  int i = 0;

#if 0
  for (i = 0; i < 15; i++)
  {
    String[i] = 65 + i + j;
  }
  String[15] = 48 + j;
  String[16] = '\0';
  LCD_Write(j, 0, String);
#else
  String[0] = 48 + j;
  String[1] = '\0';
  lcdPosition(g_lcdHandle, j, 0);
  lcdPuts(g_lcdHandle, String);
#endif

#if 0
  for (i = 0; i < 15; i++)
  {
    String[i] = 97 + i + j;
  }
  String[15] = 48 + j;
  String[16] = '\0';
  LCD_Write(j, 1, String);
#else
  String[0] = 48 + j;
  String[1] = '\0';
  lcdPosition(g_lcdHandle, j, 1);
  lcdPuts(g_lcdHandle, String);
#endif

}
#endif

//C12880
void Setup()
{
  wiringPiSetup() ;
  //Set desired pins to OUTPUT
  pinMode(SPEC_CLK, OUTPUT);
  pinMode(SPEC_ST, OUTPUT);
  //pinMode(LASER_404, OUTPUT);
  

  digitalWrite(SPEC_CLK, HIGH); // Set SPEC_CLK High
  digitalWrite(SPEC_ST, LOW); // Set SPEC_ST Low

  //LTC1865
  LTC_Init(0, 0);
  //LED
  LED_Init(LED_Ctrl1);
  LED_Init(LED_Ctrl2);
  LED_Init(LED_Ctrl3);
#if 0  //LCD
  LCD_Init();
#endif

}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */
void ReadSpectrometer(unsigned long Int_time, unsigned int * data)
{
  int delayTime = 1, counter = 0; // delay time
  long startTime = 0;

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);

  //Sample for a small amount of time
  for(int i = 0; i < 7; i++)
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

  //startTime = millis();
  startTime = micros();
  //printf("startTime = %d\n",startTime);
  //Sample for a period of time
  //for(int i = 0; i < 15; i++)
  counter = 0;

  //while ( (millis() - startTime) <= Int_time )
  while ( (micros() - startTime) <= Int_time )
  {
      counter++;
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }
  //printf("endTime = %d\n",millis());
  printf("counter = %d\n", counter);

  //Set SPEC_ST to low
  digitalWrite(SPEC_ST, LOW);

  //Sample for a period of time
  for(int i = 0; i < Period_Time; i++)
  {
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

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

}

