#include <stdio.h>
#include <wiringPi.h>

int main(void)
{

  int Led_0 = 12;
  int counter = 0;

  if (wiringPiSetup()==-1)
  {
    printf(" wiringPi Setup error \r\n");
    return -1 ;
  }

  pinMode(Led_0, OUTPUT);

  while (counter < 100)
  {
    digitalWrite(Led_0,1);
    delay(500);
    digitalWrite(Led_0,0);
    delay(500);
    counter++;
  }
}
